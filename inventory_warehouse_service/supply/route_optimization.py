"""Route Optimization Implementation"""


def calculate_distance(point_a: tuple, point_b: tuple) -> float:
    return ((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2) ** 0.5

def nearest_neighbor_route(depot: tuple, destinations: list) -> dict:
    route = [depot]
    unvisited = destinations.copy()
    current = depot
    total_distance = 0
    
    while unvisited:
        nearest = min(unvisited, key=lambda x: calculate_distance(current, x))
        distance = calculate_distance(current, nearest)
        total_distance += distance
        route.append(nearest)
        current = nearest
        unvisited.remove(nearest)
    
    total_distance += calculate_distance(current, depot)
    route.append(depot)
    
    num_stops = len(destinations)
    avg_distance = total_distance * num_stops if num_stops > 0 else 0
    
    return {
        'route': route,
        'total_distance': total_distance,
        'avg_distance': avg_distance
    }

