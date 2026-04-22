import math
from sentence_transformers import SentenceTransformer

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

def cosine_similarity(a, b) -> float:
    """Cosine similarity between two vectors (list or numpy array)."""
    dot = 0.0
    norm_a_sq = 0.0
    norm_b_sq = 0.0
    for x, y in zip(a, b):
        dot += float(x) * float(y)
        norm_a_sq += float(x) * float(x)
        norm_b_sq += float(y) * float(y)
    if norm_a_sq == 0 or norm_b_sq == 0:
        return 0.0
    return dot / (math.sqrt(norm_a_sq) * math.sqrt(norm_b_sq))


def semantic_retrieve(
    query: str,
    notes: list[str],
    note_embeddings,   # pre-computed, 2D array: one row per note
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[float, str]]:
    """
    Embed the query, score against each pre-embedded note using cosine_similarity,
    return top_k as (score, note) tuples sorted descending.
    """
    query_embedding = model.encode(query)
    scores_tuple = []

    for note, embedding in zip(notes, note_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scores_tuple.append((score, note))
    
    return sorted(scores_tuple, reverse=True)[:top_k]


if __name__ == "__main__":
    print("Loading model (first run downloads ~80MB)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding notes...")
    note_embeddings = model.encode(NOTES)
    print(f"Shape: {note_embeddings.shape}")   # expect (10, 384)

    queries = [
        "How do I handle errors that should be retried?",
        "What is cosine similarity?",
        "How does Claude call external functions?",
        "How do I manage flaky API calls?",            # NEW: tests synonyms
        "How does Claude invoke outside code?",        # NEW: tests paraphrase
    ]
    for q in queries:
        print(f"\nQ: {q}")
        for score, note in semantic_retrieve(q, NOTES, note_embeddings, model):
            print(f"  [{score:.3f}] {note}")