"""
main.py — Entry point for the Research Synthesis Tool.

This tool reads all .txt files from a folder, summarizes each one
(splitting long documents into chunks if needed), then synthesizes
all the summaries into a single briefing that identifies:
  - Key themes across the documents
  - Contradictions or tensions between them
  - Actionable recommendations

Usage:
  python main.py <input_folder>
  python main.py <input_folder> --output <output_folder>

Example:
  python main.py projects/research_synthesis/mock_data/
"""

import sys
import argparse
from dotenv import load_dotenv
import anthropic

# Load our local modules
from config import OUTPUT_DIR
from file_utils import read_txt_files, save_report
from synthesizer import summarize_document, synthesize_summaries, research_question


def parse_args():
    """
    Set up and parse command-line arguments.

    argparse is Python's built-in library for handling CLI arguments.
    It automatically generates --help text and validates input types.
    """
    parser = argparse.ArgumentParser(
        description="Synthesize multiple research documents into a unified briefing.",
        # Show the usage example in the help output
        epilog="Example: python main.py mock_data/ --output my_output/",
    )

    # Positional argument — required, no flag needed
    # The user just types the folder path after the script name
    parser.add_argument(
        "input_folder",
        help="Path to a folder containing .txt research documents",
    )

    # Optional argument — has a default value so it's not required
    parser.add_argument(
        "--output",
        default=OUTPUT_DIR,
        help=f"Where to save the output reports (default: {OUTPUT_DIR})",
    )

    return parser.parse_args()


def main():
    # ── Step 1: Load environment variables ──────────────────────────────────
    # load_dotenv() reads the .env file and makes ANTHROPIC_API_KEY available
    # to the Anthropic client. Must happen before creating the client.
    load_dotenv()

    args = parse_args()

    print("=" * 60)
    print("RESEARCH SYNTHESIS TOOL")
    print("=" * 60)

    # ── Step 2: Read all .txt files ──────────────────────────────────────────
    print(f"\nReading documents from: {args.input_folder}")
    try:
        documents = read_txt_files(args.input_folder)
    except (FileNotFoundError, ValueError) as e:
        # Print the error message and exit with a non-zero code (signals failure)
        print(f"\nError: {e}")
        sys.exit(1)

    print(f"\n  Found {len(documents)} document(s) to process.")

    # ── Step 3: Create Anthropic client ─────────────────────────────────────
    # Create the client once and pass it into functions — this is more efficient
    # than creating a new client for each API call.
    client = anthropic.Anthropic()

    # ── Step 4: Summarize each document ─────────────────────────────────────
    print("\n" + "-" * 60)
    print("STEP 1/3: Summarizing documents")
    print("-" * 60)

    doc_summaries = []
    total_input_tokens = 0
    total_output_tokens = 0

    for doc in documents:
        result = summarize_document(client, doc)
        doc_summaries.append(result)
        # Accumulate token counts across all documents
        total_input_tokens += result["tokens"]["input"]
        total_output_tokens += result["tokens"]["output"]

    # ── Step 5: Synthesize all summaries ────────────────────────────────────
    print("\n" + "-" * 60)
    print("STEP 2/3: Synthesizing into unified briefing")
    print("-" * 60)

    briefing, synth_input, synth_output = synthesize_summaries(client, doc_summaries)
    total_input_tokens += synth_input
    total_output_tokens += synth_output

    # ── Step 6: Research questions ────────────────────────────────────
    print("\n" + "-" * 60)
    print("STEP 3/3: Research questions")
    print("-" * 60)

    questions, questions_input, questions_output = research_question(client, briefing)
    total_input_tokens += questions_input
    total_output_tokens += questions_output

    # ── Step 7: Save reports ─────────────────────────────────────────────────
    print("\n" + "-" * 60)
    print("Saving reports")
    print("-" * 60)

    token_totals = {"input": total_input_tokens, "output": total_output_tokens}

    # Flatten doc_summaries for the report (remove token details from each doc)
    report_summaries = [
        {"filename": d["filename"], "summary": d["summary"], "chunks_used": d["chunks_used"]}
        for d in doc_summaries
    ]

    save_report(args.output, briefing, report_summaries, token_totals, questions)

    # ── Step 8: Print results to terminal ───────────────────────────────────
    print("\n" + "=" * 60)
    print("SYNTHESIS COMPLETE")
    print("=" * 60)

    print(f"\nOverall Summary:\n{briefing.get('overall_summary', 'N/A')}")

    print(f"\nKey Themes ({len(briefing.get('themes', []))}):")
    for theme in briefing.get("themes", []):
        print(f"  • {theme}")

    contradictions = briefing.get("contradictions", [])
    if contradictions:
        print(f"\nContradictions ({len(contradictions)}):")
        for c in contradictions:
            print(f"  ! {c}")

    print(f"\nRecommendations ({len(briefing.get('recommendations', []))}):")
    for rec in briefing.get("recommendations", []):
        print(f"  → {rec}")

    print(f"\nResearch questions ({len(questions.get('research_questions', []))})")
    for quest in questions.get("research_questions", []):
        print(f"  → {quest}")

    print(f"\nToken Usage:")
    print(f"  Input:  {total_input_tokens:,}")
    print(f"  Output: {total_output_tokens:,}")
    print(f"  Total:  {total_input_tokens + total_output_tokens:,}")


if __name__ == "__main__":
    main()
