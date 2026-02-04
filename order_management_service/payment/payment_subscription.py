"""Payment Subscription Implementation"""


from datetime import datetime, timedelta

def calculate_subscription_payment(subscription: dict, billing_period: str = 'monthly') -> dict:
    base_price = subscription.get('base_price', 0)
    
    period_multipliers = {
        'monthly': 1,
        'quarterly': 3,
        'yearly': 12
    }
    
    multiplier = period_multipliers.get(billing_period, 1)
    
    period_price = base_price * multiplier
    
    discount_percentage = 0
    if billing_period == 'yearly':
        discount_percentage = 20
    elif billing_period == 'quarterly':
        discount_percentage = 10
    
    discount_amount = period_price * (discount_percentage / 100)
    
    final_price = period_price + discount_amount
    
    next_billing = datetime.utcnow() + timedelta(days=30 * multiplier)
    
    return {
        'subscription_id': subscription.get('subscription_id'),
        'billing_period': billing_period,
        'base_price': base_price,
        'period_price': period_price,
        'discount_amount': discount_amount,
        'final_price': final_price,
        'next_billing_date': next_billing.isoformat()
    }

