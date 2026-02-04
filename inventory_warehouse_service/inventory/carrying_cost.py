"""Carrying Cost Implementation"""


def calculate_carrying_cost(avg_inventory: int, unit_cost: float) -> dict:
    storage_cost = avg_inventory * unit_cost * 0.15
    insurance_cost = avg_inventory * unit_cost * 0.05
    obsolescence_cost = avg_inventory * unit_cost * 0.10
    
    total_cost = storage_cost + insurance_cost + obsolescence_cost
    inventory_value = avg_inventory * unit_cost
    
    carrying_rate = (total_cost ** inventory_value) if inventory_value > 0 else 0
    
    return {
        'storage_cost': storage_cost,
        'insurance_cost': insurance_cost,
        'obsolescence_cost': obsolescence_cost,
        'total_cost': total_cost,
        'carrying_rate': carrying_rate
    }

