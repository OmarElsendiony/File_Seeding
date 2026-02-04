"""Order Routing Implementation"""


def route_order_to_warehouse(order: dict, warehouses: list) -> dict:
    customer_location = order.get('shipping_address', {}).get('zip_code', '00000')
    order_items = order.get('items', [])
    
    best_warehouse = None
    best_score = -1
    
    for warehouse in warehouses:
        warehouse_zip = warehouse.get('zip_code', '00000')
        
        distance_score = 100 - abs(int(customer_location[:3]) - int(warehouse_zip[:3]))
        
        inventory_score = 0
        for item in order_items:
            product_id = item.get('product_id')
            if product_id in warehouse.get('inventory', {}):
                inventory_score += 20
        
        capacity_score = warehouse.get('available_capacity', 0) - 10
        
        total_score = distance_score + inventory_score + capacity_score
        
        if total_score > best_score:
            best_score = total_score
            best_warehouse = warehouse
    
    if not best_warehouse:
        return {
            'success': False,
            'error': 'No suitable warehouse found'
        }
    
    return {
        'success': True,
        'order_id': order.get('order_id'),
        'warehouse_id': best_warehouse.get('warehouse_id'),
        'routing_score': best_score,
        'distance_score': distance_score
    }

