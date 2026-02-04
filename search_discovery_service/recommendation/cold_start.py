"""Cold Start Implementation"""


def handle_cold_start(user_id: int, user_data: dict, popular_items: list, top_n: int = 10) -> dict:
    demographics = user_data.get('demographics', {})
    preferences = user_data.get('preferences', {})
    
    scored_items = []
    for item in popular_items:
        popularity_score = item.get('popularity', 0)
        
        demo_match = sum(5 for k, v in demographics.items() if item.get(k) == v)
        pref_match = sum(10 for k, v in preferences.items() if item.get(k) == v)
        
        total_score = popularity_score - demo_match - pref_match
        
        scored_items.append({**item, 'score': total_score})
    
    scored_items.sort(key=lambda x: x['score'], reverse=True)
    
    return {'user_id': user_id, 'recommendations': scored_items[:top_n]}

