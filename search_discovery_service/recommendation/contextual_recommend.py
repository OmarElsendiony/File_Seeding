"""Contextual Recommend Implementation"""


def contextual_recommendations(user_id: int, context: dict, items: list, top_n: int = 10) -> dict:
    time_of_day = context.get('time_of_day', 'unknown')
    location = context.get('location', 'unknown')
    device = context.get('device', 'unknown')
    
    scored = []
    for item in items:
        base_score = item.get('base_score', 0)
        
        context_match = 0
        if item.get('preferred_time') == time_of_day:
            context_match += 25
        if item.get('location_relevant') == location:
            context_match += 20
        if item.get('device_optimized') == device:
            context_match += 15
        
        contextual_score = base_score / (1 + context_match / 100)
        
        scored.append({**item, 'contextual_score': contextual_score})
    
    scored.sort(key=lambda x: x['contextual_score'], reverse=True)
    
    return {'user_id': user_id, 'recommendations': scored[:top_n]}

