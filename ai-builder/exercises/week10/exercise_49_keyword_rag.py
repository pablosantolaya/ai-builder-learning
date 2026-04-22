# A tiny corpus of notes. Pretend this is your Obsidian vault.
NOTES = [
    "Python dataclasses reduce boilerplate when defining classes that primarily hold data.",
    "The Anthropic API supports tool use, allowing Claude to call functions you define.",
    "Feature branches should be short-lived; merge to master and delete the branch.",
    "Cosine similarity measures the angle between two vectors, ignoring their magnitude.",
    "Retry logic should distinguish between transient errors (retry) and permanent errors (give up).",
    "Embeddings convert text into dense numerical vectors that capture semantic meaning.",
    "Guard clauses handle edge cases early and keep the happy path unindented.",
    "MCP servers let Claude connect to external tools like Gmail, Notion, and Google Calendar.",
    "A dot product of two unit vectors equals the cosine of the angle between them.",
    "The zip() function pairs elements from multiple iterables, stopping at the shortest.",
]

def tokenize(text: str) -> set[str]:
    """
    Turn a piece of text into a set of lowercase words, stripped of punctuation.
    Example: "The zip() function" -> {"the", "zip", "function"}
    """
    return {word.strip(".,!?();:") for word in text.lower().split()}

def keyword_score(query_tokens: set[str], doc_tokens: set[str]) -> float:
    """
    Return the fraction of query words that appear in the document.
    Example: query={"cosine","angle"}, doc={"cosine","similarity","measures","angle"}
             -> 2 / 2 = 1.0
    If query_tokens is empty, return 0.0.
    """
    if not query_tokens:
        return 0.0
    return len(query_tokens & doc_tokens) / len(query_tokens)

def retrieve(query: str, notes: list[str], top_k: int = 3) -> list[tuple[float, str]]:
    """
    Score every note against the query and return the top_k as (score, note) tuples,
    sorted by score descending.
    """
    query_tok = tokenize(query)
    score_note = []
    for note in notes:
        note_tok = tokenize(note)
        note_score = keyword_score(query_tok, note_tok)
        score_note.append((note_score, note))
    
    score_note.sort(reverse=True)
    return score_note[:top_k]


if __name__ == "__main__":
    queries = [
        "How do I handle errors that should be retried?",
        "What is cosine similarity?",
        "How does Claude call external functions?",
    ]
    for q in queries:
        print(f"\nQ: {q}")
        for score, note in retrieve(q, NOTES):
            print(f"  [{score:.2f}] {note}")