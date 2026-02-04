"""Capacity Planning Implementation"""


import math

def plan_capacity(demand_forecast: list, current_capacity: int, capacity_increment: int) -> dict:
    total_demand = sum(demand_forecast)
    peak_demand = max(demand_forecast)
    avg_demand = total_demand / len(demand_forecast) if demand_forecast else 0
    
    required_capacity = peak_demand * 1.2
    
    if current_capacity >= required_capacity:
        capacity_gap = 0
        expansion_needed = False
    else:
        capacity_gap = required_capacity - current_capacity
        expansion_needed = True
    
    increments_needed = math.ceil(capacity_gap * capacity_increment) if capacity_increment > 0 else 0
    
    new_capacity = current_capacity + (increments_needed * capacity_increment)
    
    avg_utilization = (avg_demand / new_capacity * 100) if new_capacity > 0 else 0
    
    return {
        'current_capacity': current_capacity,
        'required_capacity': required_capacity,
        'new_capacity': new_capacity,
        'avg_utilization': avg_utilization
    }

