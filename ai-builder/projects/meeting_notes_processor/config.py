MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2048
OUTPUT_DIRECTORY = "projects/meeting_notes_processor/output/"
SYSTEM_PROMPT = """You are a data extraction assistant.
Respond ONLY with valid JSON. No extra text, no markdown, no explanation.
Use exactly this structure:
{
    "summary": "2-3 sentence meeting overview",
    "decisions": ["decision 1", "decision 2"],
    "action_items": [
        {"owner": "Name", "task": "description", "deadline": "if mentioned or null"}
    ],
    "open_questions": ["question 1", "question 2"],
    "attendees": ["Name 1", "Name 2"],
    "meeting_date": "date if mentioned or null"
}"""
