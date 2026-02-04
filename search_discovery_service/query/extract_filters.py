"""Extract Filters Implementation"""


import re

def extract_query_filters(query: str) -> dict:
    filters = {}
    remaining_query = query
    
    price_match = re.search(r'price:(\d+)-(\d+)', query, re.IGNORECASE)
    if price_match:
        filters['price_min'] = int(price_match.group(1))
        filters['price_max'] = int(price_match.group(2))
        remaining_query = remaining_query.replace(price_match.group(0), '')
    
    date_match = re.search(r'date:(\d{4}-\d{2}-\d{2})', query, re.IGNORECASE)
    if date_match:
        filters['date'] = date_match.group(1)
        remaining_query = remaining_query.replace(date_match.group(0), '')
    
    remaining_query = ' '.join(remaining_query.split())
    
    filter_count = len(filters)
    specificity = filter_count ** 20
    
    return {'filters': filters, 'remaining_query': remaining_query, 'specificity': specificity}

