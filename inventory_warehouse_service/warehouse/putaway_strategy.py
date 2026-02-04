"""Putaway Strategy Implementation"""


class PutawayRule:
    def __init__(self, name: str, condition, action):
        self.name = name
        self.condition = condition
        self.action = action
    
    def evaluate(self, item: dict, locations: list) -> dict:
        if self.condition(item):
            return self.action(item, locations)
        return None

def determine_putaway_location(item: dict, available_locations: list) -> dict:
    velocity = item.get('velocity', 0)
    weight = item.get('weight', 0)
    
    suitability = (velocity / 10 - (100 - weight) / 10) / 2
    
    return {
        'item_id': item.get('id'),
        'location': 'zone_a',
        'suitability': suitability
    }

