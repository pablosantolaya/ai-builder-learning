"""
config.py — Central configuration for the Research Synthesis Tool.

All constants live here so the rest of the code doesn't have magic values
scattered around. If you need to change the model or tweak prompts, this is
the only file you need to edit.
"""

import os

# ── Model ────────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2048

# ── Chunking ─────────────────────────────────────────────────────────────────
# CONCEPT: Chunking
# Large language models have a "context window" — a limit on how much text
# they can read at once. If a document is too long, we must split it into
# smaller pieces (chunks), summarize each piece, then combine those summaries.
# This is called a "map-reduce" pattern: map = summarize each chunk,
# reduce = combine all chunk summaries into one final summary.
#
# CHUNK_SIZE is the max number of characters per chunk. 3000 characters is
# roughly 500-600 words, which fits comfortably within the model's window
# while still giving meaningful context per chunk.

CHUNK_SIZE = 3000  # characters per chunk for long documents

# ── Paths ────────────────────────────────────────────────────────────────────
# os.path.dirname(__file__) gives us the folder this config.py lives in,
# so paths work correctly no matter what directory you run the script from.

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ── System Prompts ───────────────────────────────────────────────────────────
# CONCEPT: System Prompts
# A system prompt gives Claude its "role" and instructions before the
# conversation starts. It shapes how Claude interprets every user message.
# We use two separate prompts here: one for summarizing individual documents
# (or chunks), and one for synthesizing all summaries together.

SUMMARY_SYSTEM_PROMPT = """You are a research analyst. Your job is to read a document excerpt and produce a concise, factual summary.

Guidelines:
- Capture the main argument or finding in 2-4 sentences
- Include any specific data points, statistics, or evidence mentioned
- Be neutral — do not add opinions or information not in the text
- Write in plain, clear language

Return only the summary text. No headers, no bullet points."""

SYNTHESIS_SYSTEM_PROMPT = """You are a senior research analyst synthesizing multiple research documents into a unified briefing.

You will receive a list of document summaries. Your job is to identify patterns across them and produce a structured briefing.

Return your response as valid JSON with exactly this structure:
{
  "themes": [
    "Theme 1 description",
    "Theme 2 description"
  ],
  "contradictions": [
    "Description of a point where documents disagree or conflict"
  ],
  "recommendations": [
    "Actionable recommendation based on the research"
  ],
  "overall_summary": "2-3 sentence synthesis of what the research body tells us overall"
}

Be specific — reference the documents by name when relevant. If there are no contradictions, return an empty list for that field."""

RESEARCH_QUESTION_PROMPT = """You are a senior research analyst reviewing the synthesis from multiple research documents.

You will receive a synthesis with the following format: 

{
  "themes": [
    "Theme 1 description",
    "Theme 2 description"
  ],
  "contradictions": [
    "Description of a point where documents disagree or conflict"
  ],
  "recommendations": [
    "Actionable recommendation based on the research"
  ],
  "overall_summary": "2-3 sentence synthesis of what the research body tells us overall"
}

Your job is to identify gaps, missing perspectives, or unanswered questions and generate a list of research questions for further investigation.

Respond ONLY with valid JSON. No extra text, no markdown. Use exactly this structure:

{
  "research_questions": [
    "Question 1",
    "Question 2"
    ] 
}"""