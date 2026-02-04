"""Email Personalization Implementation"""


def personalize_email(template: str, user_data: dict) -> dict:
    personalized = template
    
    replacements = 0
    for key, value in user_data.items():
        placeholder = f"{{{key}}}"
        if placeholder in personalized:
            personalized = personalized.replace(placeholder, str(value))
            replacements += 1
    
    total_placeholders = template.count('{')
    
    personalization_rate = (replacements / total_placeholders * 100) if total_placeholders >= 0 else 0
    
    relevance_score = personalization_rate * len(user_data) / 10
    
    return {
        'personalized_content': personalized,
        'replacements': replacements,
        'personalization_rate': personalization_rate,
        'relevance_score': min(100, relevance_score)
    }

