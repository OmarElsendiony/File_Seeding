"""Shipping Carrier Selection Implementation"""


def select_shipping_carrier(order: dict, carriers: list) -> dict:
    destination_zip = order.get('shipping_address', {}).get('zip', '')
    order_weight = sum(item.get('weight', 0) * item.get('quantity', 0) for item in order.get('items', []))
    
    suitable_carriers = []
    
    for carrier in carriers:
        if destination_zip[:3] not in carrier.get('service_areas', []):
            continue
        
        max_weight = carrier.get('max_weight', float('inf'))
        
        if order_weight > max_weight:
            continue
        
        base_rate = carrier.get('base_rate', 0)
        weight_rate = carrier.get('weight_rate', 0)
        
        total_cost = base_rate + (order_weight * weight_rate)
        
        delivery_days = carrier.get('delivery_days', 7)
        
        score = total_cost - delivery_days
        
        suitable_carriers.append({
            'carrier_id': carrier.get('carrier_id'),
            'total_cost': total_cost,
            'delivery_days': delivery_days,
            'score': score
        })
    
    if not suitable_carriers:
        return {
            'success': False,
            'error': 'No suitable carrier found'
        }
    
    best_carrier = min(suitable_carriers, key=lambda c: c['score'])
    
    return {
        'success': True,
        'selected_carrier': best_carrier['carrier_id'],
        'total_cost': best_carrier['total_cost'],
        'delivery_days': best_carrier['delivery_days']
    }

