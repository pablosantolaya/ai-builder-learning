"""
file_utils.py — File reading and report saving for the Research Synthesis Tool.

Handles all file I/O so main.py and synthesizer.py can stay focused on
their own logic. Two responsibilities:
  1. Read all .txt files from a folder
  2. Save the final briefing as both JSON and human-readable text
"""

import os
import json
from datetime import datetime


def read_txt_files(folder_path):
    """
    Read all .txt files from a folder and return their contents.

    Args:
        folder_path (str): Path to the folder containing .txt files.

    Returns:
        list of dict: Each dict has {"filename": str, "content": str}.

    Raises:
        FileNotFoundError: If the folder doesn't exist.
        ValueError: If the folder contains no .txt files.
    """
    # Check the folder exists before trying to list it
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    # Collect all .txt files in the folder (sorted so order is predictable)
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

    if not txt_files:
        raise ValueError(f"No .txt files found in: {folder_path}")

    documents = []
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        # encoding="utf-8" handles special characters safely
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        documents.append({"filename": filename, "content": content})
        print(f"  Loaded: {filename} ({len(content):,} characters)")

    return documents


def save_report(output_dir, briefing_data, doc_summaries, token_totals, research_questions=None):
    """
    Save the synthesis results as a JSON file and a readable text report.

    Args:
        output_dir (str): Directory to write output files into.
        briefing_data (dict): The synthesis result with themes, contradictions, etc.
        doc_summaries (list): List of per-document summaries.
        token_totals (dict): Token usage counts for the full run.
        research_questions (dict, optional): Research questions generated from the synthesis.
    """
    # Create output directory if it doesn't exist (exist_ok=True means no error
    # if the folder already exists — safe to call every time)
    os.makedirs(output_dir, exist_ok=True)

    # Use a timestamp so each run creates a unique file and nothing gets overwritten
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Save JSON report ─────────────────────────────────────────────────────
    json_path = os.path.join(output_dir, f"synthesis_{timestamp}.json")
    report = {
        "generated_at": datetime.now().isoformat(),
        "token_usage": token_totals,
        "document_summaries": doc_summaries,
        "synthesis": briefing_data,
        "research_questions": research_questions or {}
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # ── Save human-readable text report ─────────────────────────────────────
    txt_path = os.path.join(output_dir, f"synthesis_{timestamp}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("RESEARCH SYNTHESIS BRIEFING\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("=" * 60 + "\n\n")

        # Overall summary first — the "so what" before the details
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(briefing_data.get("overall_summary", "N/A") + "\n\n")

        # Key themes found across documents
        f.write("KEY THEMES\n")
        f.write("-" * 40 + "\n")
        for i, theme in enumerate(briefing_data.get("themes", []), start=1):
            f.write(f"{i}. {theme}\n")
        f.write("\n")

        # Points where documents disagree — important for critical reading
        f.write("CONTRADICTIONS & TENSIONS\n")
        f.write("-" * 40 + "\n")
        contradictions = briefing_data.get("contradictions", [])
        if contradictions:
            for i, c in enumerate(contradictions, start=1):
                f.write(f"{i}. {c}\n")
        else:
            f.write("No significant contradictions identified.\n")
        f.write("\n")

        # Actionable takeaways
        f.write("RECOMMENDATIONS\n")
        f.write("-" * 40 + "\n")
        for i, rec in enumerate(briefing_data.get("recommendations", []), start=1):
            f.write(f"{i}. {rec}\n")
        f.write("\n")

        # Research questions generated from the synthesis
        if research_questions and research_questions.get("research_questions"):
            f.write("RESEARCH QUESTIONS\n")
            f.write("-" * 40 + "\n")
            for i, quest in enumerate(research_questions.get("research_questions", []), start=1):
                f.write(f"{i}. {quest}\n")
            f.write("\n")

        # Individual document summaries for reference
        f.write("DOCUMENT SUMMARIES\n")
        f.write("-" * 40 + "\n")
        for doc in doc_summaries:
            f.write(f"\n[{doc['filename']}]\n")
            f.write(doc["summary"] + "\n")

        # Token usage at the bottom
        f.write("\n" + "=" * 60 + "\n")
        f.write("TOKEN USAGE\n")
        f.write(f"  Input tokens:  {token_totals['input']:,}\n")
        f.write(f"  Output tokens: {token_totals['output']:,}\n")
        f.write(f"  Total:         {token_totals['input'] + token_totals['output']:,}\n")

    print(f"\n  JSON report: {json_path}")
    print(f"  Text report: {txt_path}")

    return txt_path
