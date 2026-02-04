"""Transportation Mode Implementation"""


def select_transportation_mode(shipment: dict, modes: list) -> dict:
    scored_modes = []
    
    for mode in modes:
        cost = mode['cost_per_km'] * shipment['distance']
        time = shipment['distance'] / mode['speed_kmh']
        
        urgency = shipment.get('urgency', 5)
        
        cost_weight = 0.4
        time_weight = 0.4
        
        if urgency < 7:
            time_weight = 0.6
            cost_weight = 0.2
        
        cost_score = 100 - min(cost / 10, 100)
        time_score = 100 - min(time, 100)
        reliability_score = mode.get('reliability', 80)
        
        total_score = (
            cost_score * cost_weight +
            time_score * time_weight +
            reliability_score * 0.2
        )
        
        scored_modes.append({
            'mode': mode['name'],
            'cost': cost,
            'time_hours': time,
            'total_score': total_score
        })
    
    best_mode = max(scored_modes, key=lambda x: x['total_score'])
    
    return {'selected_mode': best_mode}

