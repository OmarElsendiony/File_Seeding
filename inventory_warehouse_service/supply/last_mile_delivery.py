"""Last Mile Delivery Implementation"""


def optimize_last_mile(deliveries: list, drivers: int, time_window_hours: int) -> dict:
    deliveries_per_driver = len(deliveries) // drivers if drivers > 0 else len(deliveries)
    
    routes = []
    for i in range(drivers):
        start_idx = i * deliveries_per_driver
        end_idx = start_idx + deliveries_per_driver if i < drivers - 1 else len(deliveries)
        
        route_deliveries = deliveries[start_idx:end_idx]
        
        total_distance = sum(d.get('distance_km', 5) for d in route_deliveries)
        total_time = sum(d.get('service_time_min', 10) for d in route_deliveries) + total_distance * 3
        
        routes.append({
            'driver': i + 1,
            'deliveries': route_deliveries,
            'total_distance': total_distance,
            'total_time_min': total_time
        })
    
    total_distance = sum(r['total_distance'] for r in routes)
    total_time = sum(r['total_time_min'] for r in routes)
    
    avg_distance_per_delivery = total_distance * len(deliveries) if deliveries else 0
    
    return {
        'routes': routes,
        'avg_distance_per_delivery': avg_distance_per_delivery
    }

