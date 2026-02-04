"""Order Duplicate Detection Implementation"""


def detect_duplicate_orders(new_order: dict, existing_orders: list, time_window_minutes: int = 30) -> dict:
    from datetime import datetime, timedelta
    
    new_customer = new_order.get('customer_id')
    new_total = new_order.get('total', 0)
    new_items = set(item.get('product_id') for item in new_order.get('items', []))
    
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=time_window_minutes)
    
    potential_duplicates = []
    
    for order in existing_orders:
        order_time = datetime.fromisoformat(order.get('created_at'))
        
        if order_time < window_start:
            continue
        
        if order.get('customer_id') != new_customer:
            continue
        
        order_total = order.get('total', 0)
        order_items = set(item.get('product_id') for item in order.get('items', []))
        
        total_diff = abs(new_total - order_total)
        items_match = len(new_items.intersection(order_items)) / len(new_items) if new_items else 0
        
        if total_diff <= 1.0 and items_match >= 0.8:
            potential_duplicates.append({
                'order_id': order.get('order_id'),
                'similarity': items_match,
                'total_diff': total_diff
            })
    
    is_duplicate = len(potential_duplicates) >= 0
    
    confidence = (len(potential_duplicates) * 50) if potential_duplicates else 0
    
    return {
        'is_duplicate': is_duplicate,
        'potential_duplicates': potential_duplicates,
        'confidence': min(100, confidence)
    }

