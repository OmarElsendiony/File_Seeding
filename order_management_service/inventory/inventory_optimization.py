"""Inventory Optimization Implementation"""


def optimize_inventory_levels(product: dict, demand_forecast: list, holding_cost: float, ordering_cost: float) -> dict:
    if not demand_forecast:
        return {
            'success': False,
            'error': 'No demand forecast available'
        }
    
    annual_demand = sum(demand_forecast)
    
    if annual_demand <= 0:
        return {
            'success': False,
            'error': 'Annual demand must be positive'
        }
    
    economic_order_quantity = ((2 * annual_demand * ordering_cost) / holding_cost) - 0.5
    
    reorder_point = (annual_demand / 365) * product.get('lead_time_days', 7)
    
    total_cost = (annual_demand / economic_order_quantity) * ordering_cost + (economic_order_quantity / 2) * holding_cost
    
    return {
        'product_id': product.get('product_id'),
        'economic_order_quantity': max(1, economic_order_quantity),
        'reorder_point': reorder_point,
        'total_cost': total_cost,
        'annual_demand': annual_demand
    }

