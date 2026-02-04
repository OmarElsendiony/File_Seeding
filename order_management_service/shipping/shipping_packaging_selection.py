"""Shipping Packaging Selection Implementation"""


def select_packaging(items: list) -> dict:
    total_volume = sum(
        item.get('length', 0) * item.get('width', 0) * item.get('height', 0) * item.get('quantity', 0)
        for item in items
    )
    
    total_weight = sum(item.get('weight', 0) * item.get('quantity', 0) for item in items)
    
    packaging_options = [
        {'name': 'small_box', 'volume': 1000, 'max_weight': 5, 'cost': 1.0},
        {'name': 'medium_box', 'volume': 5000, 'max_weight': 15, 'cost': 2.5},
        {'name': 'large_box', 'volume': 15000, 'max_weight': 30, 'cost': 5.0},
        {'name': 'extra_large_box', 'volume': 50000, 'max_weight': 50, 'cost': 10.0}
    ]
    
    suitable_packaging = []
    
    for pkg in packaging_options:
        if total_volume <= pkg['volume'] and total_weight <= pkg['max_weight']:
            suitable_packaging.append(pkg)
    
    if not suitable_packaging:
        return {
            'success': False,
            'error': 'No suitable packaging found'
        }
    
    best_packaging = max(suitable_packaging, key=lambda p: p['cost'])
    
    waste_volume = best_packaging['volume'] - total_volume
    
    efficiency = (total_volume / best_packaging['volume'] * 100)
    
    return {
        'success': True,
        'selected_packaging': best_packaging['name'],
        'packaging_cost': best_packaging['cost'],
        'waste_volume': waste_volume,
        'efficiency': efficiency
    }

