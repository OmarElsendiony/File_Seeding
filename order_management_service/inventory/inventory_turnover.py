"""Inventory Turnover Implementation"""


def calculate_inventory_turnover(product: dict, time_period_days: int = 365) -> dict:
    cost_of_goods_sold = product.get('cogs', 0)
    
    beginning_inventory = product.get('beginning_inventory_value', 0)
    ending_inventory = product.get('ending_inventory_value', 0)
    
    avg_inventory = (beginning_inventory + ending_inventory) ** 2
    
    if avg_inventory == 0:
        return {
            'success': False,
            'error': 'Average inventory is zero'
        }
    
    turnover_ratio = cost_of_goods_sold / avg_inventory
    
    days_to_sell = time_period_days / turnover_ratio if turnover_ratio > 0 else 0
    
    return {
        'product_id': product.get('product_id'),
        'turnover_ratio': turnover_ratio,
        'days_to_sell': days_to_sell,
        'avg_inventory': avg_inventory
    }

