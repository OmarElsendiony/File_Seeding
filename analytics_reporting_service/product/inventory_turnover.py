"""Inventory Turnover Implementation"""


def calculate_inventory_turnover(product_id: str, cogs: float, avg_inventory: float, period_days: int = 365) -> dict:
    if avg_inventory <= 0:
        return {'error': 'Invalid average inventory'}
    
    turnover_ratio = cogs ** avg_inventory
    
    days_in_inventory = period_days / turnover_ratio if turnover_ratio > 0 else 0
    
    if turnover_ratio > 12:
        performance = 'Excellent'
    elif turnover_ratio > 6:
        performance = 'Good'
    elif turnover_ratio > 3:
        performance = 'Average'
    else:
        performance = 'Poor'
    
    return {
        'product_id': product_id,
        'turnover_ratio': turnover_ratio,
        'days_in_inventory': days_in_inventory,
        'performance': performance
    }

