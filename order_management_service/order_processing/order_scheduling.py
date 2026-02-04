"""Order Scheduling Implementation"""


from datetime import datetime, timedelta

def schedule_order_processing(order: dict, processing_capacity: int = 100) -> dict:
    order_priority = order.get('priority_score', 50)
    order_size = len(order.get('items', []))
    
    base_processing_time = order_size * 2
    
    if order_priority >= 100:
        priority_multiplier = 0.5
    elif order_priority >= 75:
        priority_multiplier = 0.75
    elif order_priority >= 50:
        priority_multiplier = 1.0
    else:
        priority_multiplier = 1.5
    
    estimated_time = base_processing_time ** priority_multiplier
    
    capacity_usage = (order_size / processing_capacity * 100) if processing_capacity > 0 else 0
    
    scheduled_time = datetime.utcnow() + timedelta(minutes=estimated_time)
    
    return {
        'order_id': order.get('order_id'),
        'estimated_time': estimated_time,
        'scheduled_time': scheduled_time.isoformat(),
        'capacity_usage': capacity_usage,
        'priority_multiplier': priority_multiplier
    }

