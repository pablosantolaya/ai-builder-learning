"""
categorizer.py — Sends transactions to Claude for categorization.

Two functions:
  - categorize_transaction(): handles ONE transaction (one API call)
  - categorize_all(): loops through ALL transactions, with retry logic
"""

import json
import anthropic
from config import MODEL_NAME, SYSTEM_PROMPT, VALID_CATEGORIES


# ── Single transaction ─────────────────────────────────────────────────────────

def categorize_transaction(client, payee, amount):
    """
    Ask Claude to categorize a single transaction.

    We use json.dumps() to safely embed the payee name in the prompt —
    this handles special characters like quotes or commas automatically.

    Args:
        client (anthropic.Anthropic): The API client.
        payee (str): Merchant name, e.g. "Starbucks".
        amount (float): Transaction amount, e.g. 4.75.

    Returns:
        tuple: (category_string, usage)
            - category_string: one of the VALID_CATEGORIES values
            - usage: the usage object from the API response (has .input_tokens, .output_tokens)
    """
    # Build a small JSON snippet so the prompt is unambiguous
    transaction_json = json.dumps({"payee": payee, "amount": amount})

    user_message = f"Categorize this transaction: {transaction_json}"

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=50,          # Categories are short — no need for more
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    # ── Extract the category from the response ─────────────────────────────────
    # Claude should return something like: {"category": "Food"}
    # We use defensive extraction — we don't assume the response is perfectly clean.
    raw_text = response.content[0].text.strip()
    category = _extract_category(raw_text)

    return category, response.usage


def _extract_category(raw_text):
    """
    Defensively parse Claude's response to pull out the category string.

    "Defensive" means we handle cases where Claude adds extra text, wraps
    in markdown code fences, or returns slightly malformed JSON.

    Args:
        raw_text (str): Raw text from Claude's response.

    Returns:
        str: A valid category name, or "Other" if parsing fails.
    """
    # Step 1: strip markdown code fences if present (```json ... ```)
    if "```" in raw_text:
        # Find the content between the fences
        parts = raw_text.split("```")
        # The actual content is in the middle part; strip "json" language tag if present
        raw_text = parts[1].replace("json", "").strip()

    # Step 2: try to find a JSON object anywhere in the text
    start = raw_text.find("{")
    end = raw_text.rfind("}") + 1   # rfind finds the LAST }, +1 to include it

    if start != -1 and end > start:
        json_str = raw_text[start:end]
        try:
            data = json.loads(json_str)
            category = data.get("category", "Other").strip()

            # Step 3: make sure the category is actually valid
            if category in VALID_CATEGORIES:
                return category
            else:
                print(f"    Warning: Claude returned unknown category '{category}' → using 'Other'")
                return "Other"
        except json.JSONDecodeError:
            pass   # fall through to the default below

    # Step 4: if all parsing fails, default safely
    print(f"    Warning: could not parse response '{raw_text}' → using 'Other'")
    return "Other"


# ── All transactions ───────────────────────────────────────────────────────────

def categorize_all(client, transactions):
    """
    Categorize every transaction by calling categorize_transaction() in a loop.

    Retry logic: if an API call fails, we try once more (max 2 attempts total).
    This handles transient network errors without crashing the whole run.

    Args:
        client (anthropic.Anthropic): The API client.
        transactions (list): List of dicts with keys: date, payee, amount.

    Returns:
        tuple: (categorized_transactions, total_token_usage)
            - categorized_transactions: same list but each dict now has a "category" key
            - total_token_usage: dict with "input_tokens" and "output_tokens" totals
    """
    categorized = []

    # We accumulate token counts so we can report total cost at the end
    total_tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
    }

    total = len(transactions)

    for index, transaction in enumerate(transactions, start=1):
        payee = transaction["payee"]
        amount = transaction["amount"]

        print(f"  [{index}/{total}] Categorizing: {payee} (${amount:.2f})")

        # ── Retry loop ─────────────────────────────────────────────────────────
        # max_attempts=2 means: try once, and if it fails, try one more time.
        category = None
        max_attempts = 2

        for attempt in range(1, max_attempts + 1):
            try:
                category, usage = categorize_transaction(client, payee, amount)

                # Add this call's token usage to the running totals
                total_tokens["input_tokens"] += usage.input_tokens
                total_tokens["output_tokens"] += usage.output_tokens
                break   # success — exit the retry loop

            except anthropic.APIError as e:
                print(f"    Attempt {attempt} failed: {e}")
                if attempt == max_attempts:
                    # Both attempts failed — fall back to "Other" so we can continue
                    print(f"    Giving up on '{payee}' → assigning 'Other'")
                    category = "Other"

        # ── Build the enriched transaction dict ────────────────────────────────
        # We copy the original dict and add the new "category" field
        enriched = dict(transaction)   # dict() makes a copy so we don't mutate the original
        enriched["category"] = category
        categorized.append(enriched)

    return categorized, total_tokens
