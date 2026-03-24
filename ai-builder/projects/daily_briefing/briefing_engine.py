# briefing_engine.py
# Contains all the AI logic: pre-processing data and making the two chained API calls.
# This is the core of the project — data flows in, a briefing comes out.

import json
import anthropic
from config import MODEL, MAX_TOKENS


# --- Pre-processing functions ---

def filter_unread_emails(emails):
    """
    Uses a list comprehension to keep only emails where read == False.
    List comprehension syntax: [item for item in list if condition]
    This is more concise than writing a for loop with an if statement.
    """
    return [email for email in emails if not email["read"]]


def sort_calendar(events):
    """
    Uses sorted() with a key function to order events by start_time (earliest first).
    key=lambda e: e["start_time"] means: "sort by the start_time value of each event".
    A lambda is a small, anonymous function — lambda e: e["start_time"] is the same
    as writing: def get_start_time(e): return e["start_time"]
    """
    return sorted(events, key=lambda e: e["start_time"])


# --- API Call 1: Prioritize emails ---

def call_1_prioritize_emails(client, unread_emails, focus):
    """
    First API call: sends unread emails to Claude and asks it to rank them by urgency.
    Returns the prioritized list (parsed from Claude's JSON response) and token usage.

    json.dumps() converts the Python list into a JSON string so it can be
    embedded directly inside the prompt text.
    """
    # Serialize the email list into a string we can put inside the prompt
    emails_as_string = json.dumps(unread_emails, indent=2)

    # Build the optional focus line BEFORE the prompt
    if focus is not None:
        focus_line = f"\nThe user's focus area today is '{focus}' - prioritize emails related to this topic higher.\n"
    else:
        focus_line = ""

    prompt = f"""You are an executive assistant helping prioritize a busy professional's morning.

Here are today's unread emails:
{emails_as_string}

Rank these emails by urgency and importance. {focus_line} Return ONLY a valid JSON array where each item has:
- "priority": a number from 1 (most urgent) to {len(unread_emails)} (least urgent)
- "from": the sender
- "subject": the subject line
- "reason": one sentence explaining why you gave it this priority

Return only the JSON array, no other text."""
    


    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the text content from Claude's response
    response_text = response.content[0].text

    # Try parsing directly first (happy path)
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError:
        # Claude may have added surrounding text — locate the JSON by brackets
        start = response_text.find("[")
        end   = response_text.rfind("]")

        # Fall back to single object if no array brackets found
        if start == -1 or end == -1:
            start = response_text.find("{")
            end   = response_text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(f"Could not find JSON in Claude's response: {response_text}")

        parsed = json.loads(response_text[start:end + 1])

    # Normalize: if Claude returned a single object instead of a list, wrap it
    if isinstance(parsed, dict):
        parsed = [parsed]

    prioritized = parsed

    # Capture token usage for this call
    token_usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }

    return prioritized, token_usage


# --- API Call 2: Generate the full briefing ---

def call_2_generate_briefing(client, prioritized_emails, sorted_calendar):
    """
    Second API call: takes the prioritized emails from Call 1 plus the sorted calendar
    and asks Claude to write a full morning briefing.

    This is the "chaining" part — the output of Call 1 becomes an input to Call 2.
    """
    # Serialize both data sources into strings for the prompt
    emails_as_string   = json.dumps(prioritized_emails, indent=2)
    calendar_as_string = json.dumps(sorted_calendar, indent=2)

    prompt = f"""You are an executive assistant writing a morning briefing for a busy professional.

Here are today's emails, already ranked by priority:
{emails_as_string}

Here is today's calendar:
{calendar_as_string}

Write a clear, concise morning briefing that includes:
1. A short "Good morning" opener with today's date
2. TOP PRIORITIES — the 3 most urgent emails and what action is needed
3. TODAY'S SCHEDULE — all calendar events in order with times and locations
4. WATCH LIST — any other emails worth being aware of today
5. A brief closing note

Use plain text with clear section headers. Be direct and professional."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    briefing_text = response.content[0].text

    token_usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }

    return briefing_text, token_usage


# --- Token tracking ---

def track_tokens(call1_usage, call2_usage):
    """
    Combines token counts from both API calls into a summary dict.
    Useful for understanding cost and staying within limits.
    """
    return {
        "call_1": call1_usage,
        "call_2": call2_usage,
        "total": {
            "input_tokens":  call1_usage["input_tokens"]  + call2_usage["input_tokens"],
            "output_tokens": call1_usage["output_tokens"] + call2_usage["output_tokens"]
        }
    }
