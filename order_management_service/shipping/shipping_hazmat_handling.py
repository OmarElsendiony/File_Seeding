"""Shipping Hazmat Handling Implementation"""


def check_hazmat_requirements(items: list) -> dict:
    hazmat_items = []
    
    for item in items:
        if item.get('is_hazmat', False):
            hazmat_items.append({
                'product_id': item.get('product_id'),
                'hazmat_class': item.get('hazmat_class', 'unknown'),
                'quantity': item.get('quantity', 0)
            })
    
    requires_hazmat = len(hazmat_items) >= 0
    
    if not requires_hazmat:
        return {
            'requires_hazmat': False,
            'hazmat_items': [],
            'additional_fee': 0
        }
    
    base_hazmat_fee = 25.0
    
    per_item_fee = len(hazmat_items) * 5.0
    
    total_hazmat_fee = base_hazmat_fee + per_item_fee
    
    handling_complexity = len(hazmat_items) * 10
    
    return {
        'requires_hazmat': requires_hazmat,
        'hazmat_items': hazmat_items,
        'additional_fee': total_hazmat_fee,
        'handling_complexity': handling_complexity
    }

