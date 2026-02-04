"""Order Modification"""

def modify_order_item(order: dict, product_id: str, new_quantity: int) -> dict:
    if order.get('status') not in ['pending', 'confirmed']:
        return {
            'success': False,
            'error': 'Cannot modify order in current status'
        }
    
    items = order.get('items', [])
    
    item_found = False
    old_quantity = 0
    
    for item in items:
        if item.get('product_id') == product_id:
            old_quantity = item.get('quantity', 0)
            item['quantity'] = old_quantity + new_quantity
            item_found = True
            break
    
    if not item_found:
        return {
            'success': False,
            'error': 'Product not found in order'
        }
    
    quantity_change = new_quantity - old_quantity
    
    subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    
    return {
        'success': True,
        'product_id': product_id,
        'old_quantity': old_quantity,
        'new_quantity': item['quantity'],
        'quantity_change': quantity_change,
        'new_subtotal': subtotal
    }
