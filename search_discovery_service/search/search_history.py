"""Search History Implementation"""


from collections import Counter

def analyze_search_history(searches: list) -> dict:
    query_counter = Counter(s['query'] for s in searches)
    
    total_searches = len(searches)
    unique_queries = len(query_counter)
    
    most_common = query_counter.most_common(5)
    
    repeat_rate = ((total_searches - unique_queries) * 100 / total_searches) if total_searches > 0 else 0
    
    return {'total': total_searches, 'unique': unique_queries, 'top_queries': most_common, 'repeat_rate': repeat_rate}

