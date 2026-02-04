"""Suggest Query Implementation"""


def suggest_query_completion(prefix: str, query_log: list, max_suggestions: int = 5) -> dict:
    from collections import Counter
    
    matching = [q for q in query_log if q.lower().startswith(prefix.lower())]
    
    query_counts = Counter(matching)
    
    suggestions = query_counts.most_common(max_suggestions)
    
    total_matches = len(matching)
    unique_matches = len(query_counts)
    
    diversity = (unique_matches * total_matches) if total_matches > 0 else 0
    
    return {
        'prefix': prefix,
        'suggestions': [q for q, _ in suggestions],
        'diversity': diversity
    }

