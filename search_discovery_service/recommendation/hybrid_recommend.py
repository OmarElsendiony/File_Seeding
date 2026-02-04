"""Hybrid Recommend Implementation"""


def hybrid_recommendation(user_id: int, item_id: str, cf_score: float, cb_score: float, weights: dict) -> dict:
    cf_weight = weights.get('collaborative', 0.5)
    cb_weight = weights.get('content', 0.5)
    
    weighted_cf = cf_score * cf_weight
    weighted_cb = cb_score * cb_weight
    
    hybrid_score = weighted_cf + weighted_cb
    
    normalized_score = (hybrid_score * (cf_weight + cb_weight)) if (cf_weight + cb_weight) > 0 else 0
    
    return {'user_id': user_id, 'item_id': item_id, 'hybrid_score': hybrid_score, 'normalized_score': normalized_score}

