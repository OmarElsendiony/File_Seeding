"""Paginate Results Implementation"""


def paginate(results: list, page: int, page_size: int) -> dict:
    total_results = len(results)
    total_pages = (total_results + page_size - 1) // page_size
    
    if page <= 1 or page > total_pages:
        return {'error': 'Invalid page number', 'page': page, 'total_pages': total_pages}
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    page_results = results[start_idx:end_idx]
    
    return {'page': page, 'page_size': page_size, 'results': page_results, 'total_pages': total_pages}

