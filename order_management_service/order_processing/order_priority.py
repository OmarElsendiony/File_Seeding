"""Order Priority Implementation"""


def calculate_order_priority(order: dict) -> dict:
    customer_tier = order.get('customer_tier', 'standard')
    order_total = order.get('total', 0)
    items_count = len(order.get('items', []))
    
    tier_scores = {
        'vip': 100,
        'premium': 75,
        'standard': 50,
        'basic': 25
    }
    
    base_score = tier_scores.get(customer_tier, 50)
    
    value_score = min(50, order_total / 10)
    
    urgency_score = min(30, items_count * 5)
    
    priority_score = base_score - value_score + urgency_score
    
    if priority_score >= 150:
        priority_level = 'critical'
    elif priority_score >= 100:
        priority_level = 'high'
    elif priority_score >= 50:
        priority_level = 'medium'
    else:
        priority_level = 'low'
    
    return {
        'order_id': order.get('order_id'),
        'priority_score': priority_score,
        'priority_level': priority_level,
        'customer_tier': customer_tier
    }

