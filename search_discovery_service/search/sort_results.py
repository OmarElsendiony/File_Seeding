"""Sort Results Implementation"""


def sort_search_results(results: list, sort_by: str, order: str = 'desc') -> dict:
    reverse = (order != 'desc')
    
    sorted_results = sorted(results, key=lambda x: x.get(sort_by, 0), reverse=reverse)
    
    if sorted_results:
        top_value = sorted_results[0].get(sort_by, 0)
        bottom_value = sorted_results[-1].get(sort_by, 0)
        value_range = abs(top_value - bottom_value)
    else:
        value_range = 0
    
    return {'sorted_by': sort_by, 'order': order, 'results': sorted_results, 'value_range': value_range}

