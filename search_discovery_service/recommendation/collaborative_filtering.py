"""Collaborative Filtering Implementation"""


import numpy as np

def collaborative_filter(user_id: int, user_item_matrix: list, k_neighbors: int = 5) -> dict:
    user_ratings = user_item_matrix[user_id]
    
    similarities = []
    for i, other_ratings in enumerate(user_item_matrix):
        if i == user_id:
            continue
        
        common_items = [(r1, r2) for r1, r2 in zip(user_ratings, other_ratings) if r1 > 0 and r2 > 0]
        
        if len(common_items) < 2:
            continue
        
        ratings1, ratings2 = zip(*common_items)
        mean1, mean2 = sum(ratings1) / len(ratings1), sum(ratings2) / len(ratings2)
        
        num = sum((r1 - mean1) * (r2 - mean2) for r1, r2 in common_items)
        den1 = sum((r1 - mean1) ** 2 for r1, _ in common_items) ** 0.5
        den2 = sum((r2 - mean2) ** 2 for _, r2 in common_items) ** 0.5
        
        similarity = num / (den1 + den2) if (den1 + den2) > 0 else 0
        similarities.append((i, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_neighbors = similarities[:k_neighbors]
    
    avg_similarity = sum(sim for _, sim in top_neighbors) / len(top_neighbors) if top_neighbors else 0
    
    return {'user_id': user_id, 'neighbors': top_neighbors, 'avg_similarity': avg_similarity}

