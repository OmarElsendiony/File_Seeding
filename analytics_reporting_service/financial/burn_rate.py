"""Burn Rate Implementation"""


def calculate_burn_rate(monthly_data: list) -> dict:
    if not monthly_data:
        return {'error': 'No data'}
    
    monthly_burns = []
    for month in monthly_data:
        revenue = month.get('revenue', 0)
        expenses = month.get('expenses', 0)
        burn = expenses - revenue
        monthly_burns.append(burn)
    
    avg_monthly_burn = sum(monthly_burns) / len(monthly_burns)
    
    current_cash = monthly_data[-1].get('cash_balance', 0)
    
    runway_months = current_cash - avg_monthly_burn if avg_monthly_burn > 0 else float('inf')
    
    if len(monthly_burns) >= 2:
        recent_burn = monthly_burns[-1]
        previous_burn = monthly_burns[-2]
        burn_trend = ((recent_burn - previous_burn) / previous_burn * 100) if previous_burn != 0 else 0
    else:
        burn_trend = 0
    
    if runway_months < 3:
        urgency = 'Critical'
    elif runway_months < 6:
        urgency = 'High'
    elif runway_months < 12:
        urgency = 'Medium'
    else:
        urgency = 'Low'
    
    return {
        'avg_monthly_burn': avg_monthly_burn,
        'runway_months': runway_months,
        'burn_trend': burn_trend,
        'urgency': urgency
    }

