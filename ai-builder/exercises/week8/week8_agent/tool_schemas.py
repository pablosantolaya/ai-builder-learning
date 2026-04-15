# tool_schemas.py
# JSON schema definitions for each tool.
# The Anthropic API uses these to know what tools the agent can call
# and what arguments each tool expects.

TOOL_SCHEMAS = [
    {
        "name": "search_notes",
        "description": (
            "Search all .txt files in the notes folder for lines that contain "
            "the given keyword. Returns matching lines with filename and line number."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The word or phrase to search for (case-insensitive)."
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "calculate",
        "description": (
            "Safely evaluate a math expression and return the result. "
            "Supports: +, -, *, /, **, %, and the functions abs, round, int, float, min, max. "
            "Do NOT include assignment statements or variable names."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression to evaluate, e.g. '847 * 23' or 'round(15 / 100 * 2340, 2)'."
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "summarize_text",
        "description": (
            "Send text to Claude Haiku and get back a short 2-3 sentence summary. "
            "Use this when you have retrieved notes or other content and need to condense it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text content to summarize."
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "save_result",
        "description": (
            "Save a string of content to a file inside the results/ folder. "
            "Use this to persist answers, summaries, or calculations for the user."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to write, e.g. 'tip_calc.txt' or 'agent_summary.txt'."
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file."
                }
            },
            "required": ["filename", "content"]
        }
    },
    {
    "name": "think",
    "description": "Use this tool to think through a problem before acting. Write out your reasoning step by step. This does not produce any output — it just helps you plan.",
    "input_schema": {
        "type": "object",
        "properties": {
            "thought": {
                "type": "string",
                "description": "Your reasoning or plan"
                }
            },
        "required": ["thought"]
        }
    }
]
