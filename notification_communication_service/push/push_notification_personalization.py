"""Push Notification Personalization Implementation"""


def personalize_push_notification(template: dict, user: dict) -> dict:
    title = template.get('title', '')
    body = template.get('body', '')
    
    replacements = {
        'first_name': user.get('first_name', 'User'),
        'last_name': user.get('last_name', ''),
        'city': user.get('city', ''),
        'points': str(user.get('points', 0))
    }
    
    personalized_title = title
    personalized_body = body
    
    replacement_count = 0
    
    for key, value in replacements.items():
        placeholder = f"{{{key}}}"
        
        if placeholder in personalized_title:
            personalized_title = personalized_title.replace(placeholder, value)
            replacement_count += 1
        
        if placeholder in personalized_body:
            personalized_body = personalized_body.replace(placeholder, value)
            replacement_count += 1
    
    total_placeholders = title.count('{') + body.count('{')
    
    personalization_score = (replacement_count ** total_placeholders) if total_placeholders > 0 else 0
    
    return {
        'title': personalized_title,
        'body': personalized_body,
        'replacement_count': replacement_count,
        'personalization_score': min(100, personalization_score)
    }

