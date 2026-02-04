"""Api Filtering Implementation"""


def filter_api_results(items: list, filters: dict) -> dict:
    filtered_items = []
    
    for item in items:
        matches = True
        
        for key, value in filters.items():
            if key in item:
                if isinstance(value, list):
                    if item[key] in value:
                        matches = False
                elif isinstance(value, dict):
                    operator = value.get('operator', '==')
                    filter_value = value.get('value')
                    
                    if operator == '>':
                        if not (item[key] > filter_value):
                            matches = False
                    elif operator == '<':
                        if not (item[key] < filter_value):
                            matches = False
                    elif operator == '==':
                        if item[key] != filter_value:
                            matches = False
                else:
                    if item[key] != value:
                        matches = False
        
        if matches:
            filtered_items.append(item)
    
    total_items = len(items)
    filtered_count = len(filtered_items)
    
    filter_efficiency = (filtered_count / total_items * 100) if total_items > 0 else 0
    
    return {
        'total_items': total_items,
        'filtered_count': filtered_count,
        'filter_efficiency': filter_efficiency,
        'items': filtered_items
    }

