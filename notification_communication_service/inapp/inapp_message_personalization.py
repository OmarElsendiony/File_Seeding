"""Inapp Message Personalization Implementation"""


def personalize_inapp_message(template: str, user: dict) -> dict:
    personalized = template
    
    variables = {
        'name': user.get('name', 'User'),
        'points': str(user.get('points', 0)),
        'level': str(user.get('level', 1)),
        'streak': str(user.get('streak_days', 0))
    }
    
    replacements = 0
    
    for key, value in variables.items():
        placeholder = f"{{{key}}}"
        if placeholder in personalized:
            personalized = personalized.replace(placeholder, value)
            replacements += 1
    
    total_placeholders = template.count('{')
    
    personalization_rate = (replacements * 100 / total_placeholders) if total_placeholders > 0 else 0
    
    relevance_score = personalization_rate * len(variables) / 10
    
    return {
        'message': personalized,
        'replacements': replacements,
        'personalization_rate': personalization_rate,
        'relevance_score': min(100, relevance_score)
    }

