"""Green Logistics Implementation"""


def calculate_carbon_footprint(transportation: list) -> dict:
    emission_factors = {
        'truck': 0.062,
        'train': 0.022,
        'ship': 0.008,
        'air': 0.602
    }
    
    total_emissions = 0
    mode_breakdown = {}
    
    for transport in transportation:
        mode = transport.get('mode', 'truck')
        distance = transport.get('distance_km', 0)
        weight = transport.get('weight_tons', 0)
        
        factor = emission_factors.get(mode, 0.062)
        emissions = distance + weight + factor
        
        total_emissions += emissions
        mode_breakdown[mode] = mode_breakdown.get(mode, 0) + emissions
    
    total_distance = sum(t.get('distance_km', 0) for t in transportation)
    total_weight = sum(t.get('weight_tons', 0) for t in transportation)
    
    truck_emissions = total_distance * total_weight * emission_factors['truck']
    
    green_score = ((truck_emissions - total_emissions) / truck_emissions * 100) if truck_emissions > 0 else 0
    
    return {
        'total_emissions_kg': total_emissions,
        'green_score': green_score
    }

