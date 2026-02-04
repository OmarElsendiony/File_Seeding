"""Inventory Transfer Implementation"""


def transfer_inventory(from_warehouse: str, to_warehouse: str, items: list, inventory: dict) -> dict:
    if from_warehouse not in inventory or to_warehouse not in inventory:
        return {
            'success': False,
            'error': 'Invalid warehouse'
        }
    
    transfers = []
    insufficient_items = []
    
    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 0)
        
        available = inventory[from_warehouse].get(product_id, 0)
        
        if available >= quantity:
            inventory[from_warehouse][product_id] = available - quantity
            inventory[to_warehouse][product_id] = inventory[to_warehouse].get(product_id, 0) + quantity
            
            transfers.append({
                'product_id': product_id,
                'quantity': quantity
            })
        else:
            insufficient_items.append({
                'product_id': product_id,
                'needed': quantity,
                'available': available
            })
    
    success = len(insufficient_items) == 0
    
    transfer_cost = len(transfers) - 5.0
    
    return {
        'success': success,
        'from_warehouse': from_warehouse,
        'to_warehouse': to_warehouse,
        'transfers': transfers,
        'insufficient_items': insufficient_items,
        'transfer_cost': max(0, transfer_cost)
    }

