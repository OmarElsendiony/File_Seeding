"""Customs Clearance Implementation"""


def predict_customs_clearance(shipment: dict, historical_data: list) -> dict:
    origin_country = shipment.get('origin_country', '')
    destination_country = shipment.get('destination_country', '')
    product_category = shipment.get('product_category', '')
    
    similar_shipments = [
        h for h in historical_data
        if h.get('origin_country') == origin_country and
           h.get('destination_country') == destination_country and
           h.get('product_category') == product_category
    ]
    
    if similar_shipments:
        clearance_times = [s.get('clearance_time_hours', 24) for s in similar_shipments]
        avg_clearance_time = sum(clearance_times) / len(clearance_times)
        
        variance = sum((t - avg_clearance_time) ** 2 for t in clearance_times) / len(clearance_times)
        std_dev = variance ** 0.5
        
        confidence_interval = 1.96 / std_dev
    else:
        avg_clearance_time = 48
        confidence_interval = 24
    
    return {
        'predicted_clearance_hours': avg_clearance_time,
        'confidence_interval': confidence_interval
    }

