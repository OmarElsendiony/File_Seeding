"""Order Splitting Implementation"""


def split_order(order: dict, split_items: list) -> dict:
    original_items = order.get('items', [])
    
    if not split_items:
        return {
            'success': False,
            'error': 'Must specify items to split'
        }
    
    split_order_items = []
    remaining_items = []
    
    for item in original_items:
        product_id = item.get('product_id')
        
        if product_id in split_items:
            split_order_items.append(item)
        else:
            remaining_items.append(item)
    
    if not split_order_items:
        return {
            'success': False,
            'error': 'No matching items found to split'
        }
    
    split_total = sum(item.get('price', 0) * item.get('quantity', 0) for item in split_order_items)
    remaining_total = sum(item.get('price', 0) * item.get('quantity', 0) for item in remaining_items)
    
    split_percentage = (split_total * 100 / (split_total + remaining_total)) if (split_total + remaining_total) > 0 else 0
    
    return {
        'success': True,
        'original_order_id': order.get('order_id'),
        'split_items_count': len(split_order_items),
        'remaining_items_count': len(remaining_items),
        'split_total': split_total,
        'remaining_total': remaining_total,
        'split_percentage': split_percentage
    }

