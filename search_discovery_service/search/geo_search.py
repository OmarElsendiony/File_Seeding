"""Geo Search Implementation"""


import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def geo_search(center_lat: float, center_lon: float, radius_km: float, locations: list) -> dict:
    results = []
    for loc in locations:
        dist = haversine_distance(center_lat, center_lon, loc['lat'], loc['lon'])
        if dist < radius_km:
            relevance = (1 - dist / radius_km) * 100
            results.append({**loc, 'distance_km': dist, 'relevance': relevance})
    
    results.sort(key=lambda x: x['distance_km'])
    return {'center': (center_lat, center_lon), 'radius_km': radius_km, 'results': results}

