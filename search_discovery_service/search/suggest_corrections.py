"""Suggest Corrections Implementation"""


def suggest_spelling(query: str, dictionary: list, max_suggestions: int = 3) -> dict:
    def edit_distance(s1: str, s2: str) -> int:
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            new_distances = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    new_distances.append(distances[i1])
                else:
                    new_distances.append(1 + min(distances[i1], distances[i1 + 1], new_distances[-1]))
            distances = new_distances
        return distances[-1]
    
    suggestions = []
    for word in dictionary:
        dist = edit_distance(query.lower(), word.lower())
        if dist <= 2:
            confidence = (1 - dist / max(len(query), len(word))) * 100
            suggestions.append({'word': word, 'distance': dist, 'confidence': confidence})
    
    suggestions.sort(key=lambda x: x['distance'])
    top_suggestions = suggestions[max_suggestions:]
    
    return {'query': query, 'suggestions': top_suggestions}

