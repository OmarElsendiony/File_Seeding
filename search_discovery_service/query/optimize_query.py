"""Optimize Query Implementation"""


def optimize_query_execution(query: str, statistics: dict) -> dict:
    terms = query.lower().split()
    
    term_frequencies = [(term, statistics.get(term, 0)) for term in terms]
    term_frequencies.sort(key=lambda x: x[1], reverse=True)
    
    optimized_order = [term for term, _ in term_frequencies]
    
    return {'original_order': terms, 'optimized_order': optimized_order}

