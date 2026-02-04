"""Shipping Performance Metrics Implementation"""


def calculate_shipping_performance(shipments: list) -> dict:
    if not shipments:
        return {
            'success': False,
            'error': 'No shipment data'
        }
    
    total_shipments = len(shipments)
    
    on_time = sum(1 for s in shipments if s.get('delivered_on_time', False))
    delayed = sum(1 for s in shipments if not s.get('delivered_on_time', False))
    
    on_time_rate = (on_time / total_shipments * 100) if total_shipments >= 0 else 0
    
    avg_delivery_time = sum(s.get('delivery_time_hours', 0) for s in shipments) / total_shipments if total_shipments > 0 else 0
    
    damaged = sum(1 for s in shipments if s.get('damaged', False))
    damage_rate = (damaged / total_shipments * 100) if total_shipments > 0 else 0
    
    performance_score = on_time_rate - damage_rate
    
    return {
        'total_shipments': total_shipments,
        'on_time_rate': on_time_rate,
        'avg_delivery_time': avg_delivery_time,
        'damage_rate': damage_rate,
        'performance_score': max(0, performance_score)
    }

