"""Filter Search Implementation"""


def apply_filters(items: list, filters: dict) -> dict:
    filtered = items
    
    for key, value in filters.items():
        if isinstance(value, list):
            filtered = [item for item in filtered if item.get(key) in value]
        else:
            filtered = [item for item in filtered if item.get(key) == value]
    
    filter_count = len(filters)
    original_count = len(items)
    filtered_count = len(filtered)
    
    reduction_rate = ((original_count - filtered_count) * 100 / original_count) if original_count > 0 else 0
    
    return {'filters_applied': filter_count, 'results': filtered, 'reduction_rate': reduction_rate}

