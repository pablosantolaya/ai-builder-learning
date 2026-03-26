"""
config.py — Central configuration for the Finance Analyzer.

All constants live here so they're easy to change in one place.
"""

import os

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_NAME = "claude-haiku-4-5-20251001"   # Fast, cheap model — good for batch categorization

# ── Output directory ───────────────────────────────────────────────────────────
# __file__ is the path to THIS file (config.py).
# dirname gives us the folder that contains it (finance_analyzer/).
# We store reports in a subfolder called "reports/".
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "reports")

# ── Defaults ───────────────────────────────────────────────────────────────────
DEFAULT_TOP_N = 5   # How many top transactions to highlight in the report

# ── Spending categories ────────────────────────────────────────────────────────
# Claude must return exactly one of these strings.
VALID_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Utilities",
    "Health",
    "Education",
    "Travel",
    "Subscriptions",
    "Other",
]

# ── System prompt ──────────────────────────────────────────────────────────────
# This tells Claude how to behave when categorizing transactions.
# We inject the valid category list so Claude never invents new ones.
SYSTEM_PROMPT = f"""You are a personal finance assistant that categorizes bank transactions.

When given a transaction (payee name and amount), respond with ONLY a JSON object in this exact format:
{{"category": "<category_name>"}}

Valid categories are: {", ".join(VALID_CATEGORIES)}

Rules:
- Choose the single best-matching category from the list above.
- Never invent a new category — always pick from the list.
- If nothing fits well, use "Other".
- Do not add explanations, only the JSON object.
"""
