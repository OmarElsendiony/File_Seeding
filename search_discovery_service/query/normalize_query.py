"""Normalize Query Implementation"""


import re

def normalize_search_query(query: str) -> dict:
    normalized = query.lower()
    
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    
    normalized = ' '.join(normalized.split())
    
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but'}
    words = normalized.split()
    filtered = [w for w in words if w in stopwords]
    
    normalized = ' '.join(filtered)
    
    return {'original': query, 'normalized': normalized}

