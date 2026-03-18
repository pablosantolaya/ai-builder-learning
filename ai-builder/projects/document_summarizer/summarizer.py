"""
Document Summarizer
-------------------
Reads a text file and sends it to Claude to summarize.
Saves the result as a JSON file in the output/ folder.
"""

import os
import json
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Load ANTHROPIC_API_KEY from the .env file in ai-builder/ root.
# Run this script from the ai-builder/ folder and dotenv will find it.
load_dotenv()


# ==============================================================
# FUNCTION 1: get_file_content(filepath)
#
# CONCEPT — try/except:
#   Some operations can fail at runtime. "try" runs the risky code.
#   "except SomeError" catches that specific failure so the program
#   doesn't crash — it handles the problem gracefully instead.
#
# CONCEPT — with open(...) as f:
#   Opens a file safely. Python automatically closes the file when
#   the "with" block ends, even if an error occurs inside it.
#   "r" means read-only mode.
# ==============================================================

def get_file_content(filepath):
    """Reads a text file and returns its contents as a string.
    Returns None if the file is not found."""

    try:
        # Open the file in read mode and read all text into a string
        with open(filepath, "r") as f:
            content = f.read()
        return content

    except FileNotFoundError:
        # This specific error means the path doesn't point to a real file
        print(f"Error: File not found — '{filepath}'")
        print("Please check the path and try again.")
        return None


# ==============================================================
# FUNCTION 2: get_summary_style()
#
# CONCEPT — dictionaries as lookup tables:
#   Instead of a long chain of if/elif to map "1" → a prompt string,
#   we store all the mappings in a dict. Then one line —
#   styles[choice] — does the lookup. Clean and easy to extend.
#
# CONCEPT — input():
#   Pauses the program and waits for the user to type something.
#   Always returns a string, even if they type a number.
#   .strip() removes any accidental spaces or newlines they might add.
# ==============================================================

def get_summary_style():
    """Shows a menu and returns the system prompt for the chosen style."""

    # Each key is what the user types; each value is the instruction for Claude
    styles = {
        "1": "Summarize in 2-3 sentences. Be concise.",
        "2": "Write a thorough summary with key points as bullet points.",
        "3": "Summarize using simple words a 10-year-old could understand.",
    }

    # Print the menu for the user
    print("\nChoose a summary style:")
    print("  1 — Brief (2-3 sentences)")
    print("  2 — Detailed (bullet points)")
    print("  3 — Simple (easy language)")
    print("  4 — Custom (write your own instruction)")

    # Wait for the user to type their choice
    choice = input("Enter 1, 2, 3, or 4: ").strip()

    # Option 4: let the user write their own system prompt
    if choice == "4":
        custom_prompt = input("Enter your custom instruction for Claude: ").strip()
        return custom_prompt

    # Look up the choice in the dictionary
    elif choice in styles:
        return styles[choice]
    else:
        # If they typed something unexpected, fall back to Brief
        print("Invalid choice — defaulting to Brief.")
        return styles["1"]


# ==============================================================
# FUNCTION 3: summarize_text(content, system_prompt)
#
# CONCEPT — the system prompt:
#   Claude's API separates instructions from content. The "system"
#   parameter tells Claude *how* to behave. The "messages" list
#   contains the actual content to act on. Keeping them separate
#   makes it easy to reuse the same content with different styles.
#
# CONCEPT — returning a dict instead of just the text:
#   We return a dictionary with the summary AND metadata (model name,
#   token counts). This makes it easy to pass everything to
#   save_results() later without extra arguments.
# ==============================================================

def summarize_text(content, system_prompt):
    """Sends content to Claude and returns a dict with the summary + metadata.
    Returns None if the API call fails."""

    # Read the API key that was loaded from .env
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Check the key exists before making any API call
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found. Check your .env file.")
        return None

    # Create the Anthropic client using the key
    client = anthropic.Anthropic(api_key=api_key)

    try:
        print("\nSending to Claude...")

        # Call the API — system sets the behaviour, messages holds the content
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": content}
            ]
        )

        # Pack the summary and useful metadata into a dictionary
        results = {
            "summary": response.content[0].text,
            "model": response.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return results

    except anthropic.AuthenticationError:
        print("Error: Invalid API key. Check your ANTHROPIC_API_KEY.")
        return None
    except anthropic.APIConnectionError:
        print("Error: Can't connect to the API. Check your internet.")
        return None
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None


# ==============================================================
# FUNCTION 4: save_results(results, output_dir)
#
# CONCEPT — datetime for timestamps:
#   datetime.now() gives the current date and time as an object.
#   .strftime() formats it as a string using pattern codes:
#     %Y = 4-digit year, %m = month, %d = day
#     %H = hour, %M = minute, %S = second
#   So strftime("%Y%m%d_%H%M%S") → "20260318_143022"
#
# CONCEPT — json.dump():
#   Converts a Python dictionary into JSON text and writes it to
#   a file. indent=4 adds spacing so the file is human-readable.
# ==============================================================

def save_results(results, output_dir):
    """Saves the results dictionary as a JSON file with a timestamp in the name.
    Returns the path of the saved file."""

    # Build a timestamp string like "20260318_143022"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Combine the output folder path and the filename into one full path
    filename = f"summary_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # Write the dictionary to the file as formatted JSON
    with open(filepath, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to: {filepath}")
    return filepath


# ==============================================================
# FUNCTION 5: main()
#
# CONCEPT — orchestration:
#   main() doesn't do any work itself — it just calls the other
#   functions in the right order and passes results between them.
#   Checking for None after each step lets us stop early if
#   something went wrong, instead of crashing later.
#
# CONCEPT — if __name__ == "__main__":
#   When Python runs a file directly, it sets __name__ to "__main__".
#   This guard means main() only runs when you execute this file
#   directly — not if another file imports it.
# ==============================================================

def main():
    """Orchestrates all steps: read file → choose style → summarize → save."""

    print("=== Document Summarizer ===")

    # Step 1: Ask the user for the file to summarize
    filepath = input("\nEnter the path to your text file: ").strip()

    # Step 2: Read the file — stop if it wasn't found
    content = get_file_content(filepath)
    if content is None:
        return

    print(f"File loaded. ({len(content)} characters)")

    # Step 3: Ask the user how they want it summarized
    system_prompt = get_summary_style()

    # Step 4: Send to Claude — stop if the API call failed
    results = summarize_text(content, system_prompt)
    if results is None:
        return

    # Step 5: Print the summary to the screen
    print("\n--- Summary ---")
    print(results["summary"])

    # Step 6: Print token usage
    print(f"\nTokens used — input: {results['input_tokens']}, output: {results['output_tokens']}")

    # Step 7: Save results to the output/ folder
    save_results(results, "projects/document_summarizer/output")


if __name__ == "__main__":
    main()
