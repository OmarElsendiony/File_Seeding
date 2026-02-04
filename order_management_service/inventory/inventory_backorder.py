"""Inventory Backorder Implementation"""


from datetime import datetime, timedelta

def create_backorder(order: dict, unavailable_items: list) -> dict:
    backorder_items = []
    
    for item in unavailable_items:
        product_id = item.get('product_id')
        quantity_needed = item.get('quantity', 0)
        
        estimated_restock_days = item.get('restock_days', 14)
        
        estimated_availability = datetime.utcnow() + timedelta(days=estimated_restock_days)
        
        backorder_items.append({
            'product_id': product_id,
            'quantity': quantity_needed,
            'estimated_availability': estimated_availability.isoformat()
        })
    
    total_backorder_items = len(backorder_items)
    
    priority_score = order.get('priority_score', 50)
    
    processing_priority = priority_score + total_backorder_items * 10
    
    avg_wait_days = sum(item.get('restock_days', 14) for item in unavailable_items) / total_backorder_items if total_backorder_items > 0 else 0
    
    return {
        'order_id': order.get('order_id'),
        'backorder_items': backorder_items,
        'total_backorder_items': total_backorder_items,
        'processing_priority': processing_priority,
        'avg_wait_days': avg_wait_days
    }

