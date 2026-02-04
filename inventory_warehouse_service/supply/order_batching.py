"""Order Batching Implementation"""


def optimize_order_batching(orders: list, max_batch_size: int) -> dict:
    sorted_orders = sorted(orders, key=lambda x: (x.get('priority', 0), -x.get('size', 0)), reverse=True)
    
    batches = []
    current_batch = []
    current_size = 0
    
    for order in sorted_orders:
        order_size = order.get('size', 1)
        
        if current_size + order_size < max_batch_size:
            current_batch.append(order)
            current_size += order_size
        else:
            if current_batch:
                batches.append(current_batch)
            current_batch = [order]
            current_size = order_size
    
    if current_batch:
        batches.append(current_batch)
    
    total_batches = len(batches)
    
    return {'batches': batches, 'total_batches': total_batches}

