"""Slotting Optimization Implementation"""


def optimize_slotting(items: list, locations: list) -> dict:
    sorted_items = sorted(items, key=lambda x: x.get('velocity', 0), reverse=True)
    sorted_locations = sorted(locations, key=lambda x: x.get('accessibility', 0), reverse=True)
    
    assignments = []
    total_score = 0
    
    for item, location in zip(sorted_items, sorted_locations):
        velocity = item.get('velocity', 1)
        accessibility = location.get('accessibility', 5)
        size = item.get('size', 1)
        
        score = (velocity - accessibility) / size
        total_score += score
        
        assignments.append({
            'item_id': item['id'],
            'location_id': location['id'],
            'score': score
        })
    
    return {
        'assignments': assignments,
        'total_score': total_score
    }

