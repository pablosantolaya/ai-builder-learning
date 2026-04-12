"""
synthesizer.py — Claude API calls for the Research Synthesis Tool.

Three responsibilities:
  1. chunk_text()        — split long documents into manageable pieces (no API)
  2. summarize_document() — summarize one document (with chunking if needed)
  3. synthesize_summaries() — find themes, contradictions, recommendations

CONCEPT: Map-Reduce Summarization
When a document is too long to summarize in one API call, we use a two-step
approach inspired by the "map-reduce" pattern from data processing:
  - MAP step: send each chunk to Claude separately and get a chunk summary
  - REDUCE step: send all chunk summaries together and get one final summary

This lets us handle documents of any length, not just short ones.
"""

import json
import anthropic
from config import MODEL, MAX_TOKENS, CHUNK_SIZE, SUMMARY_SYSTEM_PROMPT, SYNTHESIS_SYSTEM_PROMPT, RESEARCH_QUESTION_PROMPT


def chunk_text(content, chunk_size=CHUNK_SIZE):
    """
    Split a long string into chunks of at most chunk_size characters.

    We split on paragraph boundaries (double newlines) where possible so
    chunks don't cut a sentence in half. If a paragraph itself is longer
    than chunk_size, it gets its own chunk.

    Args:
        content (str): The full document text.
        chunk_size (int): Max characters per chunk.

    Returns:
        list of str: The chunks. If content fits in one chunk, returns [content].
    """
    # If the document is short enough, no chunking needed
    if len(content) <= chunk_size:
        return [content]

    # Split into paragraphs (double newline = paragraph break)
    paragraphs = content.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit, save current chunk and start fresh
        if current_chunk and len(current_chunk) + len(paragraph) + 2 > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            # Add paragraph to current chunk (with blank line separator)
            current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def _call_api(client, system_prompt, user_message):
    """
    Make a single API call and return (response_text, input_tokens, output_tokens).

    This helper keeps the API call details in one place so summarize_document()
    and synthesize_summaries() don't repeat the same boilerplate.

    Args:
        client: Anthropic client instance.
        system_prompt (str): The system prompt.
        user_message (str): The user message content.

    Returns:
        tuple: (response_text, input_tokens, output_tokens)
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    return text, input_tokens, output_tokens


def summarize_document(client, doc):
    """
    Summarize a single document, using chunking if it's too long.

    For short documents: one API call → one summary.
    For long documents:
      Step 1 (MAP): summarize each chunk individually
      Step 2 (REDUCE): combine chunk summaries into one final summary

    Args:
        client: Anthropic client instance.
        doc (dict): {"filename": str, "content": str}

    Returns:
        dict: {
            "filename": str,
            "summary": str,
            "chunks_used": int,   # 1 for short docs, N for chunked docs
            "tokens": {"input": int, "output": int}
        }
    """
    filename = doc["filename"]
    content = doc["content"]
    total_input = 0
    total_output = 0

    # Split document into chunks (returns [content] if short enough)
    chunks = chunk_text(content)

    print(f"\n  Processing: {filename}")

    if len(chunks) == 1:
        # ── Short document: one direct summary ──────────────────────────────
        print(f"    → Single call (document fits in one chunk)")
        message = f"Please summarize this document:\n\n{chunks[0]}"
        summary, inp, out = _call_api(client, SUMMARY_SYSTEM_PROMPT, message)
        total_input += inp
        total_output += out

    else:
        # ── Long document: MAP then REDUCE ───────────────────────────────────
        print(f"    → Chunked into {len(chunks)} parts (MAP step)")

        # MAP: summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks, start=1):
            print(f"    → Summarizing chunk {i}/{len(chunks)}...")
            message = (
                f"This is part {i} of {len(chunks)} of the document '{filename}'.\n"
                f"Please summarize this excerpt:\n\n{chunk}"
            )
            chunk_summary, inp, out = _call_api(client, SUMMARY_SYSTEM_PROMPT, message)
            chunk_summaries.append(f"[Part {i}] {chunk_summary}")
            total_input += inp
            total_output += out

        # REDUCE: combine chunk summaries into one final summary
        print(f"    → Combining chunk summaries (REDUCE step)")
        combined = "\n\n".join(chunk_summaries)
        message = (
            f"The following are summaries of each section of the document '{filename}'.\n"
            f"Write a single unified summary that captures the overall document:\n\n{combined}"
        )
        summary, inp, out = _call_api(client, SUMMARY_SYSTEM_PROMPT, message)
        total_input += inp
        total_output += out

    print(f"    ✓ Done ({total_input + total_output:,} tokens used)")

    return {
        "filename": filename,
        "summary": summary,
        "chunks_used": len(chunks),
        "tokens": {"input": total_input, "output": total_output},
    }


def synthesize_summaries(client, doc_summaries):
    """
    Take all document summaries and produce a unified research briefing.

    CONCEPT: Synthesis Prompting
    We're asking Claude to do higher-order reasoning here — not just "what does
    this document say?" but "how do these documents relate to each other?"
    This means looking for:
      - Themes: ideas that appear across multiple documents
      - Contradictions: places where documents disagree or tension exists
      - Recommendations: what action the research body suggests

    Args:
        client: Anthropic client instance.
        doc_summaries (list): List of dicts from summarize_document().

    Returns:
        tuple: (briefing_dict, input_tokens, output_tokens)
            briefing_dict has keys: themes, contradictions, recommendations, overall_summary
    """
    print("\n  Synthesizing all summaries into final briefing...")

    # Format all summaries into a clear numbered list for the prompt
    formatted = ""
    for i, doc in enumerate(doc_summaries, start=1):
        formatted += f"Document {i}: {doc['filename']}\n{doc['summary']}\n\n"

    message = (
        f"I have {len(doc_summaries)} research documents. "
        f"Here are their summaries:\n\n{formatted}"
        f"Please synthesize these into a unified briefing."
    )

    response_text, input_tokens, output_tokens = _call_api(
        client, SYNTHESIS_SYSTEM_PROMPT, message
    )

    # ── Parse JSON response ──────────────────────────────────────────────────
    # Claude sometimes wraps JSON in markdown code fences (```json ... ```)
    # so we strip those before parsing.
    clean = response_text.strip()
    if clean.startswith("```"):
        # Remove the opening fence (```json or ```) and closing fence (```)
        clean = clean.split("\n", 1)[-1]  # remove first line
        clean = clean.rsplit("```", 1)[0]  # remove last fence

    try:
        briefing = json.loads(clean)
    except json.JSONDecodeError:
        # If JSON parsing fails, return the raw text in a safe structure
        print("  Warning: Could not parse JSON response — saving raw text.")
        briefing = {
            "themes": [],
            "contradictions": [],
            "recommendations": [],
            "overall_summary": response_text,
        }

    print(f"  ✓ Synthesis complete ({input_tokens + output_tokens:,} tokens used)")

    return briefing, input_tokens, output_tokens


def research_question(client, synthesis_doc):
    synthesis_doc_string = json.dumps(synthesis_doc, indent=2)
    response_text, input_tokens, output_tokens = _call_api(
        client, RESEARCH_QUESTION_PROMPT, synthesis_doc_string
    )

    clean = response_text.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1]
        clean = clean.rsplit("```", 1)[0]

    try:
        questions = json.loads(clean)
    except json.JSONDecodeError:
        print("  Warning: Could not parse JSON response — saving raw text.")
        questions = {
            "research_questions": []
        }
    print(f" Research questions complete ({input_tokens + output_tokens:,} tokens used)")

    return questions, input_tokens, output_tokens