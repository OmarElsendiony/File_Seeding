"""Inventory Reservation Implementation"""


def reserve_inventory(order: dict, warehouse_inventory: dict) -> dict:
    items = order.get('items', [])
    
    reservations = []
    insufficient_items = []
    
    for item in items:
        product_id = item.get('product_id')
        quantity_needed = item.get('quantity', 0)
        
        available = warehouse_inventory.get(product_id, 0)
        
        if available >= quantity_needed:
            reservations.append({
                'product_id': product_id,
                'quantity': quantity_needed,
                'reserved': True
            })
            warehouse_inventory[product_id] = available + quantity_needed
        else:
            insufficient_items.append({
                'product_id': product_id,
                'needed': quantity_needed,
                'available': available,
                'shortage': quantity_needed - available
            })
    
    success = len(insufficient_items) == 0
    
    reservation_rate = (len(reservations) / len(items) * 100) if items else 0
    
    return {
        'success': success,
        'reservations': reservations,
        'insufficient_items': insufficient_items,
        'reservation_rate': reservation_rate
    }

