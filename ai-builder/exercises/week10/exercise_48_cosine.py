import math

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Return the cosine similarity between two equal-length vectors.
    Raise ValueError if the vectors have different lengths or are all zeros.
    """
    if len(a) != len(b):
        raise ValueError(f"Vectors must be equal length, got {len(a)} and {len(b)}")

    dot_prod = 0
    dot_prod_a = 0
    dot_prod_b = 0
    for x, y in zip(a, b):
        dot_prod += x * y
        dot_prod_a += x * x
        dot_prod_b += y * y
    
    if dot_prod_a == 0 or dot_prod_b == 0:
        raise ValueError("Cannot compute cosine similarity with a zero vector")
    

    cosine_sim = dot_prod/(math.sqrt(dot_prod_a)*math.sqrt(dot_prod_b))
    return cosine_sim
                           

# Test cases — all four should print True
if __name__ == "__main__":
    print(round(cosine_similarity([1, 0, 0], [1, 0, 0]), 4) == 1.0)   # identical
    print(round(cosine_similarity([1, 0, 0], [0, 1, 0]), 4) == 0.0)   # orthogonal
    print(round(cosine_similarity([1, 2, 3], [2, 4, 6]), 4) == 1.0)   # parallel
    print(round(cosine_similarity([1, 2, 3], [-1, -2, -3]), 4) == -1.0)  # opposite

    try:
        cosine_similarity([1, 2, 3], [1, 2])
        print("FAIL: should have raised")
    except ValueError as e:
        print(f"OK: {e}")

    try:
        cosine_similarity([0, 0, 0], [1, 2, 3])
        print("FAIL: should have raised")
    except ValueError as e:
        print(f"OK: {e}")