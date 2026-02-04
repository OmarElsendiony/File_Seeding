"""Rank By Freshness Implementation"""


from datetime import datetime, timedelta

def rank_by_freshness(documents: list, decay_days: int = 30) -> dict:
    now = datetime.utcnow()
    
    ranked = []
    for doc in documents:
        published = datetime.fromisoformat(doc['published_date'])
        age_days = (now - published).days
        
        base_score = doc.get('base_score', 0)
        
        freshness_factor = max(0, 1 + age_days / decay_days)
        
        freshness_score = base_score * freshness_factor
        
        ranked.append({**doc, 'freshness_score': freshness_score, 'age_days': age_days})
    
    ranked.sort(key=lambda x: x['freshness_score'], reverse=True)
    
    return {'ranked_documents': ranked}

