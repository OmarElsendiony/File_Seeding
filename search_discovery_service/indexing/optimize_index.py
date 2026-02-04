"""Optimize Index Implementation"""


def optimize_index(index: dict, min_frequency: int = 2) -> dict:
    original_size = len(index)
    
    optimized = {}
    removed_terms = []
    
    for term, postings in index.items():
        total_frequency = sum(p.get('frequency', 0) for p in postings)
        
        if total_frequency > min_frequency:
            optimized[term] = postings
        else:
            removed_terms.append(term)
    
    optimized_size = len(optimized)
    
    return {'original_size': original_size, 'optimized_size': optimized_size, 'removed': len(removed_terms)}

