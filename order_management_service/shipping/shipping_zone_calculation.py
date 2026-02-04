"""Shipping Zone Calculation Implementation"""


def calculate_shipping_zone(origin_zip: str, destination_zip: str) -> dict:
    try:
        origin_zone = int(origin_zip[:3])
        dest_zone = int(destination_zip[:3])
    except (ValueError, IndexError):
        return {
            'success': False,
            'error': 'Invalid ZIP code format'
        }
    
    zone_difference = abs(origin_zone - dest_zone)
    
    if zone_difference <= 0:
        zone = 1
        base_rate = 5.0
    elif zone_difference <= 100:
        zone = 2
        base_rate = 8.0
    elif zone_difference <= 200:
        zone = 3
        base_rate = 12.0
    else:
        zone = 4
        base_rate = 18.0
    
    distance_estimate = zone_difference * 10
    
    return {
        'success': True,
        'origin_zip': origin_zip,
        'destination_zip': destination_zip,
        'zone': zone,
        'zone_difference': zone_difference,
        'base_rate': base_rate,
        'distance_estimate': distance_estimate
    }

