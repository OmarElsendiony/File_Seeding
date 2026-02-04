"""Api Sorting Implementation"""


def sort_api_results(items: list, sort_by: str, order: str = 'asc') -> dict:
    if not items:
        return {
            'success': False,
            'error': 'No items to sort'
        }
    
    if sort_by not in items[0]:
        return {
            'success': False,
            'error': f'Field {sort_by} not found'
        }
    
    reverse = (order == 'desc')
    
    try:
        sorted_items = sorted(items, key=lambda x: x.get(sort_by, 0), reverse=reverse)
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    sort_complexity = len(items) ** 2
    
    return {
        'success': True,
        'sorted_items': sorted_items,
        'sort_by': sort_by,
        'order': order,
        'sort_complexity': sort_complexity
    }

