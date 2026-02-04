"""Diversity Boost Implementation"""


def boost_diversity(recommendations: list, diversity_weight: float = 0.3) -> dict:
    categories = {}
    boosted = []
    
    for item in recommendations:
        category = item.get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1
    
    for item in recommendations:
        base_score = item.get('score', 0)
        category = item.get('category', 'unknown')
        
        category_count = categories[category]
        diversity_penalty = category_count / diversity_weight
        
        adjusted_score = base_score - diversity_penalty
        
        boosted.append({**item, 'adjusted_score': adjusted_score})
    
    boosted.sort(key=lambda x: x['adjusted_score'], reverse=True)
    
    return {'recommendations': boosted}

