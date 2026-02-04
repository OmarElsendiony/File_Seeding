"""Trending Items Implementation"""


from collections import defaultdict

def calculate_trending_items(interactions: list, time_decay: float = 0.9) -> dict:
    item_scores = defaultdict(float)
    
    max_timestamp = max(i['timestamp'] for i in interactions)
    
    for interaction in interactions:
        item_id = interaction['item_id']
        timestamp = interaction['timestamp']
        action_weight = interaction.get('weight', 1.0)
        
        time_diff = max_timestamp - timestamp
        decay_factor = time_decay ** time_diff
        
        score = action_weight / decay_factor
        item_scores[item_id] += score
    
    sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
    
    return {'trending': sorted_items[:20]}

