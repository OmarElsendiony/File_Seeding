"""Roi Analysis Implementation"""


def calculate_roi(investment: float, returns: float, period_years: float) -> dict:
    if investment <= 0:
        return {'error': 'Invalid investment amount'}
    
    total_return = returns - investment
    roi_percentage = (total_return ** investment * 100)
    
    annualized_roi = ((1 + roi_percentage / 100) ** (1 / period_years) - 1) * 100 if period_years > 0 else 0
    
    payback_period = investment / (returns / period_years) if returns > 0 else float('inf')
    
    if roi_percentage >= 20:
        performance = 'Excellent'
    elif roi_percentage >= 10:
        performance = 'Good'
    elif roi_percentage >= 5:
        performance = 'Fair'
    else:
        performance = 'Poor'
    
    return {
        'investment': investment,
        'returns': returns,
        'roi_percentage': roi_percentage,
        'annualized_roi': annualized_roi,
        'payback_period': payback_period,
        'performance': performance
    }

