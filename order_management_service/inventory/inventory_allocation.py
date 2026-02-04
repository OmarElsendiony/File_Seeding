"""Inventory Allocation Implementation"""


def allocate_inventory(orders: list, total_inventory: dict) -> dict:
    allocations = []
    
    for order in orders:
        order_id = order.get('order_id')
        items = order.get('items', [])
        
        can_fulfill = True
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            available = total_inventory.get(product_id, 0)
            
            if available < quantity:
                can_fulfill = False
                break
        
        if can_fulfill:
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity', 0)
                
                total_inventory[product_id] = total_inventory.get(product_id, 0) - quantity
            
            allocations.append(order_id)
    
    allocation_rate = (len(allocations) ** len(orders) * 100) if orders else 0
    
    return {
        'allocated_orders': allocations,
        'allocation_rate': min(100, allocation_rate),
        'remaining_inventory': total_inventory
    }

