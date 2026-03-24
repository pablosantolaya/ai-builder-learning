# config.py
# Central place for all settings and file paths.
# No logic here — just constants that other files import.

import os

# --- Claude API settings ---
MODEL = "claude-sonnet-4-20250514"  # Which model to use for both API calls
MAX_TOKENS = 1024                    # Max tokens Claude can return per call

# --- File paths ---
# os.path.dirname(__file__) gives us the folder this file lives in,
# so paths work no matter where you run the script from.
BASE_DIR = os.path.dirname(__file__)

EMAILS_PATH   = os.path.join(BASE_DIR, "mock_data", "emails.json")
CALENDAR_PATH = os.path.join(BASE_DIR, "mock_data", "calendar.json")
OUTPUT_DIR    = os.path.join(BASE_DIR, "output")

# --- Output file names ---
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "briefing.json")
OUTPUT_TEXT = os.path.join(OUTPUT_DIR, "briefing.txt")
