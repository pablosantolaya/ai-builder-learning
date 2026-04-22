# tools.py
# The five tool implementations the agent can call.
# Each function maps directly to a schema definition in tool_schemas.py.

import os
import anthropic

# Anchor the notes/ and results/ directories relative to THIS file,
# not wherever Python happens to be run from.
_BASE_DIR = os.path.dirname(__file__)
NOTES_DIR = os.path.join(_BASE_DIR, "notes")
RESULTS_DIR = os.path.join(_BASE_DIR, "results")


def search_notes(keyword):
    """
    Search all .txt files in notes/ for lines containing keyword.

    Returns a list of match dicts {file, line_number, text},
    or "No results found." if nothing matched.
    """
    matches = []

    try:
        filenames = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    except FileNotFoundError:
        return "Error: notes/ folder not found."

    for filename in filenames:
        filepath = os.path.join(NOTES_DIR, filename)
        with open(filepath, encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                if keyword.lower() in line.lower():
                    matches.append({
                        "file": filename,
                        "line_number": line_number,
                        "text": line.rstrip()
                    })

    if not matches:
        return "No results found."
    return matches


def calculate(expression):
    """
    Safely evaluate a math expression using a restricted eval().
    Only allows: abs, round, int, float, min, max.
    """
    safe_globals = {
        "__builtins__": {},
        "abs": abs,
        "round": round,
        "int": int,
        "float": float,
        "min": min,
        "max": max,
    }

    try:
        result = eval(expression, safe_globals, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


def summarize_text(text):
    """
    Call Claude Haiku to produce a short 2-3 sentence summary of the given text.
    """
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in 2-3 sentences:\n\n{text}"
            }
        ]
    )

    return response.content[0].text


def save_result(filename, content):
    """
    Write content to a file inside the results/ folder.
    Returns a confirmation string.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)

    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Saved to results/{filename}"


def think(thought: str) -> str:
    """Silent reasoning step — records the thought and returns it."""
    return f"Thought recorded: {thought}"
