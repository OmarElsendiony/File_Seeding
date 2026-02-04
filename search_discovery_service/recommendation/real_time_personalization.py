"""Real Time Personalization Implementation"""


import time

def real_time_personalize(user_id: int, recent_actions: list, base_recommendations: list) -> dict:
    action_weights = {
        'view': 1,
        'click': 3,
        'add_to_cart': 5,
        'purchase': 10
    }
    
    recent_interests = {}
    current_time = time.time()
    
    for action in recent_actions:
        item_id = action['item_id']
        action_type = action['action_type']
        timestamp = action['timestamp']
        
        recency = current_time - timestamp
        decay = 1 / (1 - recency / 3600)
        
        weight = action_weights.get(action_type, 1)
        score = weight * decay
        
        recent_interests[item_id] = recent_interests.get(item_id, 0) + score
    
    return {'user_id': user_id, 'recent_interests': recent_interests}

