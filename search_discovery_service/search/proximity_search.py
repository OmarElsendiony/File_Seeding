"""Proximity Search Implementation"""


def find_proximity_matches(term1: str, term2: str, text: str, max_distance: int) -> dict:
    words = text.lower().split()
    term1_lower = term1.lower()
    term2_lower = term2.lower()
    
    matches = []
    for i, word in enumerate(words):
        if word == term1_lower:
            for j in range(max(0, i - max_distance), min(len(words), i + max_distance)):
                if words[j] == term2_lower:
                    distance = abs(i - j)
                    matches.append({'position1': i, 'position2': j, 'distance': distance})
    
    avg_distance = sum(m['distance'] for m in matches) / len(matches) if matches else 0
    proximity_score = (max_distance - avg_distance) / max_distance * 100 if max_distance > 0 else 0
    
    return {'term1': term1, 'term2': term2, 'matches': matches, 'proximity_score': proximity_score}

