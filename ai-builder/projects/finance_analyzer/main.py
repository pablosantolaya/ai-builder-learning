"""
main.py — Entry point for the Personal Finance Analyzer.

Usage:
    python main.py mock_data/transactions.csv
    python main.py mock_data/transactions.csv --output reports/ --top-n 10

Flow:
    1. Parse command-line arguments
    2. Read and validate the CSV file
    3. Categorize each transaction with Claude
    4. Calculate spending summary
    5. Save JSON + text reports
    6. Print token usage
"""

import os
import sys
import json
import argparse
from datetime import datetime

import anthropic
from dotenv import load_dotenv

# We use __file__ to make imports work regardless of where the script is run from.
# This adds the finance_analyzer/ folder to Python's search path.
sys.path.insert(0, os.path.dirname(__file__))

from config import OUTPUT_DIR, DEFAULT_TOP_N
from file_utils import read_and_validate_csv, save_json_report, save_text_report
from categorizer import categorize_all
from analyzer import calculate_summary


def main():
    # ── Load environment variables (.env file with ANTHROPIC_API_KEY) ──────────
    load_dotenv()

    # ── Parse command-line arguments ───────────────────────────────────────────
    # argparse handles --flags and positional arguments automatically.
    parser = argparse.ArgumentParser(
        description="Analyze personal finance transactions using Claude AI."
    )

    # Positional argument — required, no -- prefix
    parser.add_argument(
        "input_file",
        help="Path to the CSV bank export file (e.g. mock_data/transactions.csv)"
    )

    # Optional arguments — have defaults so they're not required
    parser.add_argument(
        "--output",
        default=OUTPUT_DIR,
        help=f"Directory to save reports (default: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--top-n",
        type=int,           # argparse will convert the string to int for us
        default=DEFAULT_TOP_N,
        dest="top_n",       # stores it as args.top_n (not args.top-n, which is invalid Python)
        help=f"Number of top transactions to show (default: {DEFAULT_TOP_N})"
    )

    args = parser.parse_args()

    # ── Resolve the input file path relative to this script ───────────────────
    # If the user passes a relative path like "mock_data/transactions.csv",
    # we resolve it relative to finance_analyzer/ so it works from any directory.
    script_dir = os.path.dirname(__file__)
    input_path = os.path.join(script_dir, args.input_file) if not os.path.isabs(args.input_file) else args.input_file

    print(f"\n{'='*50}")
    print("   PERSONAL FINANCE ANALYZER")
    print(f"{'='*50}")
    print(f"Input file : {input_path}")
    print(f"Output dir : {args.output}")
    print(f"Top N      : {args.top_n}")
    print()

    # ── Step 1: Read and validate CSV ──────────────────────────────────────────
    print("[ Step 1 ] Reading CSV...")
    valid_transactions, errors = read_and_validate_csv(input_path)

    # Print any validation errors so the user knows which rows were skipped
    if errors:
        print(f"  {len(errors)} row(s) skipped due to validation errors:")
        for error in errors:
            print(f"    ! {error}")

    print(f"  {len(valid_transactions)} valid transactions loaded.\n")

    if not valid_transactions:
        print("No valid transactions found. Exiting.")
        return

    # ── Step 2: Categorize with Claude ────────────────────────────────────────
    print("[ Step 2 ] Categorizing transactions with Claude...")
    client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from environment automatically

    categorized_transactions, token_usage = categorize_all(client, valid_transactions)
    print()

    # ── Step 3: Calculate summary ──────────────────────────────────────────────
    print("[ Step 3 ] Calculating summary...")
    summary = calculate_summary(categorized_transactions, top_n=args.top_n)
    print(f"  Total spending:  ${summary['total_spending']:.2f}")
    print(f"  Categories used: {summary['category_count']}")
    print(f"  Daily average:   ${summary['daily_average']:.2f}")
    print()

    # ── Step 4: Save reports ───────────────────────────────────────────────────
    print("[ Step 4 ] Saving reports...")

    # Timestamp used in filenames so each run produces a unique file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build the full report dict — this is what gets written to the JSON file
    report = {
        "generated_at": timestamp,
        "input_file":   input_path,
        "summary":      summary,
        "transactions": categorized_transactions,
    }

    save_json_report(report, args.output, timestamp)
    save_text_report(report, args.output, timestamp)
    print()

    # ── Step 5: Print token usage ──────────────────────────────────────────────
    print("[ Token Usage ]")
    print(f"  Input tokens:  {token_usage['input_tokens']:,}")    # :, adds thousands separator
    print(f"  Output tokens: {token_usage['output_tokens']:,}")
    print(f"  Total tokens:  {token_usage['input_tokens'] + token_usage['output_tokens']:,}")
    print()
    print("Done!")


# ── Script guard ───────────────────────────────────────────────────────────────
# This block only runs when you execute the file directly (python main.py).
# It does NOT run when another file imports main.py as a module.
if __name__ == "__main__":
    main()
