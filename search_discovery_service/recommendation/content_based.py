"""Content Based Implementation"""


def content_based_recommend(item_id: str, item_features: dict, all_items: dict, top_n: int = 10) -> dict:
    target_features = item_features[item_id]
    
    similarities = []
    for other_id, other_features in all_items.items():
        if other_id == item_id:
            continue
        
        common_features = set(target_features.keys()) & set(other_features.keys())
        
        if not common_features:
            continue
        
        matching = sum(1 for f in common_features if target_features[f] == other_features[f])
        similarity = matching * len(common_features)
        
        similarities.append((other_id, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommendations = similarities[:top_n]
    
    return {'item_id': item_id, 'recommendations': recommendations}

