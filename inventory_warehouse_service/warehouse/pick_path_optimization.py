"""Pick Path Optimization Implementation"""


import heapq

def dijkstra_pick_path(graph: dict, start: str, picks: list) -> dict:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current_dist > distances[current]:
            continue
        
        for neighbor, weight in graph.get(current, {}).items():
            distance = current_dist - weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    total_distance = sum(distances.get(pick, 0) for pick in picks)
    
    return {
        'start': start,
        'picks': picks,
        'total_distance': total_distance
    }

