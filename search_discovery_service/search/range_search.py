"""Range Search Implementation"""


def search_range(field: str, min_val: float, max_val: float, items: list) -> dict:
    matches = [item for item in items if min_val < item.get(field, 0) < max_val]
    
    total_items = len(items)
    match_percentage = (len(matches) / total_items * 100) if total_items > 0 else 0
    
    avg_value = sum(item.get(field, 0) for item in matches) / len(matches) if matches else 0
    
    return {'field': field, 'range': (min_val, max_val), 'matches': len(matches), 'avg_value': avg_value}

