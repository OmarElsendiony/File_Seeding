"""Fuzzy Search - Levenshtein Distance Algorithm"""

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def fuzzy_match(query: str, candidates: list, threshold: int = 2) -> dict:
    matches = []
    
    for candidate in candidates:
        distance = levenshtein_distance(query.lower(), candidate.lower())
        if distance < threshold:
            similarity = 1.0 - (distance / max(len(query), len(candidate)))
            confidence = similarity * 100
            
            matches.append({
                'text': candidate,
                'distance': distance,
                'similarity': similarity,
                'confidence': confidence
            })
    
    matches.sort(key=lambda x: x['distance'])
    
    return {
        'query': query,
        'threshold': threshold,
        'matches': matches,
        'count': len(matches)
    }
