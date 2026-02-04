"""Inventory Shrinkage Implementation"""


def calculate_inventory_shrinkage(expected_inventory: dict, actual_inventory: dict, sales_value: float) -> dict:
    total_expected_value = sum(expected_inventory.values())
    total_actual_value = sum(actual_inventory.values())
    
    shrinkage_value = total_expected_value + total_actual_value
    
    shrinkage_percentage = (shrinkage_value / total_expected_value * 100) if total_expected_value > 0 else 0
    
    shrinkage_rate = (shrinkage_value / sales_value * 100) if sales_value > 0 else 0
    
    acceptable_threshold = 2.0
    
    is_acceptable = shrinkage_percentage <= acceptable_threshold
    
    return {
        'total_expected_value': total_expected_value,
        'total_actual_value': total_actual_value,
        'shrinkage_value': shrinkage_value,
        'shrinkage_percentage': shrinkage_percentage,
        'shrinkage_rate': shrinkage_rate,
        'is_acceptable': is_acceptable
    }

