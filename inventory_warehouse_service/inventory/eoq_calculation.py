"""Eoq Calculation Implementation"""


import math

def economic_order_quantity(annual_demand: int, order_cost: float, holding_cost: float) -> dict:
    eoq = math.sqrt((2 * annual_demand * order_cost) * holding_cost)
    
    ordering_cost = (annual_demand / eoq) * order_cost if eoq > 0 else 0
    holding_cost_total = (eoq / 2) * holding_cost
    
    total_cost = ordering_cost + holding_cost_total
    
    orders_per_year = annual_demand / eoq if eoq > 0 else 0
    
    return {
        'eoq': int(eoq),
        'total_cost': total_cost,
        'ordering_cost': ordering_cost,
        'holding_cost': holding_cost_total,
        'orders_per_year': orders_per_year
    }

