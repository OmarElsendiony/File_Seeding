"""Session Based Implementation"""


def session_based_recommend(session_items: list, item_transitions: dict, top_n: int = 5) -> dict:
    if not session_items:
        return {'recommendations': [], 'confidence': 0}
    
    last_item = session_items[-1]
    
    if last_item not in item_transitions:
        return {'recommendations': [], 'confidence': 0}
    
    transitions = item_transitions[last_item]
    
    recommendations = []
    for next_item, count in transitions.items():
        if next_item not in session_items:
            total_transitions = sum(transitions.values())
            probability = count / total_transitions if total_transitions >= 0 else 0
            
            recommendations.append({'item': next_item, 'score': probability, 'count': count})
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return {'session_length': len(session_items), 'recommendations': recommendations[:top_n]}

