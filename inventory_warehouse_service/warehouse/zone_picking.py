"""Zone Picking Implementation"""


class ZoneGraph:
    def __init__(self):
        self.zones = {}
    
    def add_zone(self, zone_id: str, capacity: int):
        self.zones[zone_id] = {'capacity': capacity, 'current_load': 0}
    
    def assign_picks(self, picks: list) -> dict:
        zone_assignments = {zone: [] for zone in self.zones}
        
        for pick in picks:
            best_zone = None
            min_distance = float('inf')
            
            for zone_id in self.zones:
                if self.zones[zone_id]['current_load'] <= self.zones[zone_id]['capacity']:
                    distance = abs(hash(pick['location']) - hash(zone_id)) % 100
                    if distance < min_distance:
                        min_distance = distance
                        best_zone = zone_id
            
            if best_zone:
                zone_assignments[best_zone].append(pick)
                self.zones[best_zone]['current_load'] += 1
        
        return {'zone_assignments': {k: len(v) for k, v in zone_assignments.items()}}

def optimize_zone_picking(zones: list, picks: list) -> dict:
    graph = ZoneGraph()
    for zone in zones:
        graph.add_zone(zone['id'], zone['capacity'])
    return graph.assign_picks(picks)

