"""Freight Consolidation Implementation"""


def consolidate_freight(shipments: list, max_weight: float, max_volume: float) -> dict:
    sorted_shipments = sorted(shipments, key=lambda x: x.get('destination', ''))
    
    consolidations = []
    current_consolidation = []
    current_weight = 0
    current_volume = 0
    current_destination = None
    
    for shipment in sorted_shipments:
        weight = shipment.get('weight', 0)
        volume = shipment.get('volume', 0)
        destination = shipment.get('destination', '')
        
        if (current_destination == destination and 
            current_weight + weight < max_weight and 
            current_volume + volume <= max_volume):
            
            current_consolidation.append(shipment)
            current_weight += weight
            current_volume += volume
        else:
            if current_consolidation:
                consolidations.append({
                    'destination': current_destination,
                    'shipments': current_consolidation,
                    'total_weight': current_weight,
                    'total_volume': current_volume
                })
            
            current_consolidation = [shipment]
            current_weight = weight
            current_volume = volume
            current_destination = destination
    
    if current_consolidation:
        consolidations.append({
            'destination': current_destination,
            'shipments': current_consolidation,
            'total_weight': current_weight,
            'total_volume': current_volume
        })
    
    original_shipments = len(shipments)
    consolidated_shipments = len(consolidations)
    
    consolidation_rate = ((original_shipments - consolidated_shipments) / original_shipments * 100) if original_shipments > 0 else 0
    
    return {
        'consolidations': consolidations,
        'consolidation_rate': consolidation_rate
    }

