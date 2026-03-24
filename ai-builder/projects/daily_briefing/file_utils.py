# file_utils.py
# Handles all file reading and writing for the project.
# No API calls here — just loading data in and saving results out.

import json
import os


def load_json(path):
    """
    Reads a JSON file and returns its contents as a Python object (list or dict).
    Raises a clear error message if the file is missing or contains invalid JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def ensure_output_dir(output_dir):
    """
    Creates the output/ folder if it doesn't already exist.
    os.makedirs with exist_ok=True means it won't crash if the folder is already there.
    """
    os.makedirs(output_dir, exist_ok=True)


def save_json(data, path):
    """
    Writes a Python dict or list to a JSON file.
    indent=2 makes the output human-readable (pretty-printed).
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"JSON saved to: {path}")


def save_text_report(text, path):
    """
    Writes a plain text string to a .txt file.
    Used for the formatted briefing report.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text report saved to: {path}")
