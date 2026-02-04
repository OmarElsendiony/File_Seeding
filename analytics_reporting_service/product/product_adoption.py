"""Product Adoption Implementation"""


def analyze_product_adoption(product: dict, user_data: list) -> dict:
    from datetime import datetime
    
    launch_date = datetime.fromisoformat(product.get('launch_date', '2024-01-01'))
    
    adopters = []
    for user in user_data:
        first_use = user.get('first_use_date')
        if first_use:
            first_use_date = datetime.fromisoformat(first_use)
            days_to_adopt = (first_use_date - launch_date).days
            
            adopters.append({
                'user_id': user['id'],
                'days_to_adopt': days_to_adopt
            })
    
    if not adopters:
        return {'error': 'No adopters'}
    
    total_adopters = len(adopters)
    
    early_adopters = sum(1 for a in adopters if a['days_to_adopt'] < 30)
    early_majority = sum(1 for a in adopters if 30 < a['days_to_adopt'] <= 90)
    late_majority = sum(1 for a in adopters if 90 < a['days_to_adopt'] <= 180)
    laggards = sum(1 for a in adopters if a['days_to_adopt'] > 180)
    
    adoption_curve = {
        'early_adopters': (early_adopters / total_adopters * 100),
        'early_majority': (early_majority / total_adopters * 100),
        'late_majority': (late_majority / total_adopters * 100),
        'laggards': (laggards / total_adopters * 100)
    }
    
    avg_days_to_adopt = sum(a['days_to_adopt'] for a in adopters) / total_adopters
    
    return {
        'product_id': product['id'],
        'total_adopters': total_adopters,
        'adoption_curve': adoption_curve,
        'avg_days_to_adopt': avg_days_to_adopt
    }

