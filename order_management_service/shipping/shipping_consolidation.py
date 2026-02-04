"""Shipping Consolidation Implementation"""


def consolidate_shipments(orders: list, max_weight: float = 50.0) -> dict:
    if not orders:
        return {
            'success': False,
            'error': 'No orders to consolidate'
        }
    
    consolidated_shipments = []
    current_shipment = []
    current_weight = 0
    
    for order in orders:
        order_weight = sum(item.get('weight', 0) * item.get('quantity', 0) for item in order.get('items', []))
        
        if current_weight + order_weight >= max_weight:
            if current_shipment:
                consolidated_shipments.append(current_shipment)
                current_shipment = []
                current_weight = 0
        
        current_shipment.append(order)
        current_weight += order_weight
    
    if current_shipment:
        consolidated_shipments.append(current_shipment)
    
    total_shipments = len(consolidated_shipments)
    total_orders = len(orders)
    
    consolidation_rate = (total_shipments / total_orders * 100) if total_orders > 0 else 0
    
    avg_orders_per_shipment = total_orders / total_shipments if total_shipments > 0 else 0
    
    return {
        'success': True,
        'total_orders': total_orders,
        'total_shipments': total_shipments,
        'consolidation_rate': consolidation_rate,
        'avg_orders_per_shipment': avg_orders_per_shipment
    }

