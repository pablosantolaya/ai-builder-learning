# main.py
# Entry point for the daily briefing generator.
# Handles CLI arguments, orchestrates the data flow, and saves the outputs.

import os
import argparse
import anthropic
from dotenv import load_dotenv

from config import EMAILS_PATH, CALENDAR_PATH, OUTPUT_DIR
from file_utils import load_json, ensure_output_dir, save_json, save_text_report
from briefing_engine import (
    filter_unread_emails,
    sort_calendar,
    call_1_prioritize_emails,
    call_2_generate_briefing,
    track_tokens
)


def parse_args():
    """
    Defines the CLI interface using argparse.
    All arguments are optional — defaults come from config.py.
    Run: python main.py --help  to see all options.
    """
    parser = argparse.ArgumentParser(description="Generate a daily briefing from emails and calendar.")

    parser.add_argument(
        "--emails",
        default=EMAILS_PATH,
        help="Path to the emails JSON file (default: mock_data/emails.json)"
    )
    parser.add_argument(
        "--calendar",
        default=CALENDAR_PATH,
        help="Path to the calendar JSON file (default: mock_data/calendar.json)"
    )
    parser.add_argument(
        "--output-dir",
        default=OUTPUT_DIR,
        help="Folder to save output files (default: output/)"
    )
    parser.add_argument(
        "--focus",
        help="Focus area to prioritize (e.g., finance, operations)"
    )

    # Mutually exclusive flags: user can ask for JSON only or text only
    # If neither is passed, both outputs are saved
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "--json-only",
        action="store_true",
        help="Save only the JSON output"
    )
    output_group.add_argument(
        "--text-only",
        action="store_true",
        help="Save only the text report"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # --- Load environment variables from .env file ---
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found. Make sure it's set in your .env file.")

    # --- Step 1: Load raw data ---
    print("Loading data...")
    emails   = load_json(args.emails)
    calendar = load_json(args.calendar)

    # --- Step 2: Pre-process with list comprehensions ---
    unread_emails = filter_unread_emails(emails)
    sorted_events = sort_calendar(calendar)

    print(f"  {len(emails)} emails loaded — {len(unread_emails)} unread")
    print(f"  {len(calendar)} calendar events loaded")

    # --- Step 3: API Call 1 — prioritize unread emails ---
    print("\nCall 1: Prioritizing emails...")
    client = anthropic.Anthropic(api_key=api_key)
    prioritized_emails, tokens_call1 = call_1_prioritize_emails(client, unread_emails,args.focus)
    print(f"  Tokens used — input: {tokens_call1['input_tokens']}, output: {tokens_call1['output_tokens']}")

    # --- Step 4: API Call 2 — generate full briefing ---
    print("\nCall 2: Generating briefing...")
    briefing_text, tokens_call2 = call_2_generate_briefing(client, prioritized_emails, sorted_events)
    print(f"  Tokens used — input: {tokens_call2['input_tokens']}, output: {tokens_call2['output_tokens']}")

    # --- Step 5: Track total token usage ---
    token_summary = track_tokens(tokens_call1, tokens_call2)
    print(f"\nTotal tokens — input: {token_summary['total']['input_tokens']}, output: {token_summary['total']['output_tokens']}")

    # --- Step 6: Save outputs ---
    # Build output paths from args.output_dir so --output-dir override is respected
    ensure_output_dir(args.output_dir)
    output_json_path = os.path.join(args.output_dir, "briefing.json")
    output_text_path = os.path.join(args.output_dir, "briefing.txt")

    # Build the JSON output — combines the briefing text and all supporting data
    output_data = {
        "briefing": briefing_text,
        "prioritized_emails": prioritized_emails,
        "sorted_calendar": sorted_events,
        "token_usage": token_summary
    }

    if not args.text_only:
        save_json(output_data, output_json_path)

    if not args.json_only:
        save_text_report(briefing_text, output_text_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
