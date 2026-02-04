"""Customer Loyalty Implementation"""


def calculate_loyalty_score(customer: dict) -> dict:
    tenure_months = customer.get('tenure_months', 0)
    purchase_count = customer.get('purchase_count', 0)
    avg_order_value = customer.get('avg_order_value', 0)
    referrals = customer.get('referral_count', 0)
    reviews = customer.get('review_count', 0)
    
    tenure_score = min(tenure_months / 12 * 25, 25)
    purchase_score = min(purchase_count / 10 * 25, 25)
    value_score = min(avg_order_value / 100 * 25, 25)
    advocacy_score = min((referrals * 5 + reviews * 3) / 20 * 25, 25)
    
    loyalty_score = tenure_score + purchase_score + value_score + advocacy_score
    
    if loyalty_score > 80:
        tier = 'Platinum'
    elif loyalty_score >= 60:
        tier = 'Gold'
    elif loyalty_score >= 40:
        tier = 'Silver'
    else:
        tier = 'Bronze'
    
    return {
        'customer_id': customer.get('id'),
        'loyalty_score': loyalty_score,
        'loyalty_tier': tier
    }

