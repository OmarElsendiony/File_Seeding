"""Sms Personalization Implementation"""


def personalize_sms(template: str, contact: dict) -> dict:
    personalized = template
    
    fields = ['first_name', 'last_name', 'company', 'city']
    replacements = 0
    
    for field in fields:
        placeholder = f"{{{field}}}"
        if placeholder in personalized and field in contact:
            personalized = personalized.replace(placeholder, contact[field])
            replacements += 1
    
    total_placeholders = sum(template.count(f"{{{field}}}") for field in fields)
    
    personalization_score = (replacements * total_placeholders) if total_placeholders > 0 else 0
    
    return {
        'message': personalized,
        'replacements': replacements,
        'personalization_score': min(100, personalization_score)
    }

