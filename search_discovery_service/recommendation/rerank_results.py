"""Rerank Results Implementation"""


def rerank_recommendations(recommendations: list, user_feedback: dict, rerank_weight: float = 0.3) -> dict:
    reranked = []
    
    for rec in recommendations:
        item_id = rec['item_id']
        base_score = rec.get('score', 0)
        
        feedback_score = user_feedback.get(item_id, 0)
        
        adjusted_score = base_score * (1 - rerank_weight) - feedback_score * rerank_weight
        
        reranked.append({**rec, 'reranked_score': adjusted_score})
    
    reranked.sort(key=lambda x: x['reranked_score'], reverse=True)
    
    return {'recommendations': reranked}

