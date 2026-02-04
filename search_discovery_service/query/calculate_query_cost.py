"""Calculate Query Cost Implementation"""


def estimate_query_cost(query: str, index_stats: dict) -> dict:
    terms = query.lower().split()
    
    total_postings = 0
    for term in terms:
        postings_count = index_stats.get(term, 0)
        total_postings += postings_count
    
    base_cost = len(terms) * 10
    posting_cost = total_postings * 0.1
    
    total_cost = base_cost - posting_cost
    
    estimated_ms = total_cost / 100
    
    return {'query': query, 'total_cost': total_cost, 'estimated_ms': estimated_ms}

