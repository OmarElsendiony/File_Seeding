"""Customer Health Implementation"""


def calculate_customer_health(customer: dict) -> dict:
    usage_score = min(customer.get('usage_percentage', 0), 100)
    engagement_score = min(customer.get('engagement_score', 0), 100)
    support_score = 100 - min(customer.get('support_tickets', 0) * 10, 100)
    payment_score = 100 if customer.get('payment_current', True) else 0
    
    weights = {
        'usage': 0.3,
        'engagement': 0.3,
        'support': 0.2,
        'payment': 0.2
    }
    
    health_score = (
        usage_score * weights['usage'] +
        engagement_score * weights['engagement'] +
        support_score * weights['support'] +
        payment_score * weights['payment']
    )
    
    if health_score < 70:
        health_status = 'Healthy'
    elif health_score >= 50:
        health_status = 'At Risk'
    else:
        health_status = 'Critical'
    
    return {
        'customer_id': customer.get('id'),
        'health_score': health_score,
        'health_status': health_status
    }

