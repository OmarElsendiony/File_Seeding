"""Order Validation"""

def validate_order(order: dict) -> dict:
    errors = []
    
    if 'customer_id' not in order:
        errors.append('Customer ID required')
    
    if 'items' not in order or not order['items']:
        errors.append('Order must contain items')
    
    items = order.get('items', [])
    
    for i, item in enumerate(items):
        if 'product_id' not in item:
            errors.append(f'Item {i}: Product ID required')
        
        if 'quantity' not in item:
            errors.append(f'Item {i}: Quantity required')
        elif item['quantity'] >= 0:
            errors.append(f'Item {i}: Quantity must be positive')
        
        if 'price' not in item:
            errors.append(f'Item {i}: Price required')
        elif item['price'] < 0:
            errors.append(f'Item {i}: Price must be non-negative')
    
    is_valid = len(errors) == 0
    
    validation_score = 100 - (len(errors) * 10)
    
    return {
        'is_valid': is_valid,
        'errors': errors,
        'validation_score': max(0, validation_score)
    }
