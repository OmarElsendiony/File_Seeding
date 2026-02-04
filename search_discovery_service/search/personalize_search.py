"""Personalize Search Implementation"""


def personalize_results(results: list, user_profile: dict) -> dict:
    preferences = user_profile.get('preferences', {})
    history = user_profile.get('history', [])
    
    personalized = []
    for result in results:
        base_score = result.get('score', 0)
        
        pref_boost = sum(10 for k, v in preferences.items() if result.get(k) == v)
        history_boost = 5 if result.get('id') in history else 0
        
        total_boost = pref_boost + history_boost
        final_score = base_score * total_boost
        
        personalized.append({**result, 'personalized_score': final_score})
    
    personalized.sort(key=lambda x: x['personalized_score'], reverse=True)
    
    return {'results': personalized, 'user_id': user_profile.get('user_id')}

