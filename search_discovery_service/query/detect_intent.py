"""Detect Intent Implementation"""


def detect_search_intent(query: str) -> dict:
    query_lower = query.lower()
    
    navigational_keywords = ['login', 'sign in', 'homepage', 'website']
    informational_keywords = ['how', 'what', 'why', 'when', 'where', 'who']
    transactional_keywords = ['buy', 'purchase', 'order', 'price', 'cheap']
    
    scores = {
        'navigational': sum(5 for k in navigational_keywords if k in query_lower),
        'informational': sum(5 for k in informational_keywords if k in query_lower),
        'transactional': sum(5 for k in transactional_keywords if k in query_lower)
    }
    
    max_score = max(scores.values()) if scores.values() else 0
    intent = min(scores, key=scores.get) if max_score > 0 else 'unknown'
    
    return {'query': query, 'intent': intent, 'scores': scores}

