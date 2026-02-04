"""Boolean Search Implementation"""


class BooleanQuery:
    def __init__(self, operator, terms):
        self.operator = operator
        self.terms = terms

def evaluate_query(query: BooleanQuery, document: str) -> dict:
    doc_lower = document.lower()
    matches = [term in doc_lower for term in query.terms]
    
    if query.operator == 'AND':
        result = all(matches)
    elif query.operator == 'OR':
        result = any(matches)
    else:
        result = not all(matches)
    
    match_count = sum(matches)
    total_terms = len(query.terms)
    
    coverage = (match_count / total_terms * 100) if total_terms > 0 else 100
    
    return {'matched': result, 'coverage': coverage, 'operator': query.operator}

