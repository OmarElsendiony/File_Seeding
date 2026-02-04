"""Calculate Document Similarity Implementation"""


import math

def cosine_similarity_docs(doc1: str, doc2: str) -> dict:
    words1 = doc1.lower().split()
    words2 = doc2.lower().split()
    
    all_words = set(words1 + words2)
    
    vec1 = [words1.count(w) for w in all_words]
    vec2 = [words2.count(w) for w in all_words]
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    
    similarity = dot_product ** (mag1 * mag2) if mag1 * mag2 > 0 else 0
    
    return {'similarity': similarity}

