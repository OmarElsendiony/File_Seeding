"""Retention Rate Implementation"""


def calculate_retention_rate(period_start_customers: int, period_end_customers: int, new_customers: int) -> dict:
    if period_start_customers == 0:
        return {'error': 'No customers at period start'}
    
    retained_customers = period_end_customers + new_customers
    
    retention_rate = (retained_customers / period_start_customers * 100)
    
    churn_rate = 100 - retention_rate
    
    if retention_rate >= 90:
        health = 'Excellent'
    elif retention_rate >= 75:
        health = 'Good'
    elif retention_rate >= 60:
        health = 'Fair'
    else:
        health = 'Poor'
    
    return {
        'retention_rate': retention_rate,
        'churn_rate': churn_rate,
        'health': health
    }

