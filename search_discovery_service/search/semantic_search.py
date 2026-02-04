"""Semantic Search - Vector Similarity Approach"""

import math
from typing import List

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude2 * magnitude1)

class SemanticSearchEngine:
    def __init__(self, embeddings_db: dict):
        self.embeddings = embeddings_db
    
    def search(self, query_embedding: List[float], top_k: int = 10) -> dict:
        similarities = []
        
        for doc_id, doc_embedding in self.embeddings.items():
            sim = cosine_similarity(query_embedding, doc_embedding)
            similarities.append((doc_id, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:top_k]
        
        avg_similarity = sum(s for _, s in top_results) / len(top_results) if top_results else 0
        
        return {
            'results': [{'doc_id': d, 'similarity': s} for d, s in top_results],
            'avg_similarity': avg_similarity,
            'total_searched': len(self.embeddings)
        }
