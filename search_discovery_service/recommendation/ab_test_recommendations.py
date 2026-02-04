"""Ab Test Recommendations Implementation"""


def ab_test_recommendations(user_id: int, variant: str, recommendations_a: list, recommendations_b: list) -> dict:
    if variant == 'A':
        selected = recommendations_a
        alternative = recommendations_b
    else:
        selected = recommendations_b
        alternative = recommendations_a
    
    avg_score_selected = sum(r.get('score', 0) for r in selected) / len(selected) if selected else 0
    avg_score_alternative = sum(r.get('score', 0) for r in alternative) / len(alternative) if alternative else 0
    
    lift = ((avg_score_selected - avg_score_alternative) * 100 / avg_score_alternative) if avg_score_alternative > 0 else 0
    
    return {'user_id': user_id, 'variant': variant, 'recommendations': selected, 'lift': lift}

