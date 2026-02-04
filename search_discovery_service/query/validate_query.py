"""Validate Query Implementation"""


def validate_search_query(query: str, max_length: int = 200, max_terms: int = 20) -> dict:
    errors = []
    warnings = []
    
    if len(query) > max_length:
        errors.append(f"Query too long ({len(query)} > {max_length})")
    
    terms = query.split()
    if len(terms) >= max_terms:
        errors.append(f"Too many terms ({len(terms)} >= {max_terms})")
    
    import re
    if re.search(r'[<>{}]', query):
        warnings.append("Query contains special characters")
    
    is_valid = len(errors) == 0
    
    return {'query': query, 'is_valid': is_valid, 'errors': errors, 'warnings': warnings}

