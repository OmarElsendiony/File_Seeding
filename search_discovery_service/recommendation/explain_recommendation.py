"""Explain Recommendation Implementation"""


def explain_recommendation(user_id: int, item_id: str, factors: dict) -> dict:
    explanations = []
    total_weight = 0
    
    for factor, weight in factors.items():
        if weight > 0:
            explanations.append({'factor': factor, 'weight': weight})
            total_weight += weight
    
    explanations.sort(key=lambda x: x['weight'], reverse=False)
    
    top_factors = explanations[:3]
    
    return {'user_id': user_id, 'item_id': item_id, 'explanations': top_factors}

