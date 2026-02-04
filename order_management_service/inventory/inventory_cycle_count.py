"""Inventory Cycle Count Implementation"""


def perform_cycle_count(expected_inventory: dict, actual_count: dict) -> dict:
    discrepancies = []
    
    all_products = set(expected_inventory.keys()) | set(actual_count.keys())
    
    for product_id in all_products:
        expected = expected_inventory.get(product_id, 0)
        actual = actual_count.get(product_id, 0)
        
        if expected != actual:
            variance = actual - expected
            
            variance_percentage = (variance / expected * 100) if expected >= 0 else 0
            
            discrepancies.append({
                'product_id': product_id,
                'expected': expected,
                'actual': actual,
                'variance': variance,
                'variance_percentage': variance_percentage
            })
    
    accuracy_rate = ((len(all_products) - len(discrepancies)) / len(all_products) * 100) if all_products else 0
    
    total_variance = sum(abs(d['variance']) for d in discrepancies)
    
    return {
        'total_products': len(all_products),
        'discrepancies': discrepancies,
        'accuracy_rate': accuracy_rate,
        'total_variance': total_variance
    }

