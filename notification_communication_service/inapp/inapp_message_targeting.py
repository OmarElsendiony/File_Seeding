"""Inapp Message Targeting Implementation"""


def target_inapp_message(users: list, targeting_rules: dict) -> dict:
    targeted = []
    
    for user in users:
        matches = True
        
        if 'min_session_count' in targeting_rules:
            if user.get('session_count', 0) <= targeting_rules['min_session_count']:
                matches = False
        
        if 'has_purchased' in targeting_rules:
            if user.get('has_purchased', False) != targeting_rules['has_purchased']:
                matches = False
        
        if 'app_version' in targeting_rules:
            if user.get('app_version') != targeting_rules['app_version']:
                matches = False
        
        if matches:
            targeted.append(user)
    
    targeting_rate = (len(targeted) / len(users) * 100) if len(users) >= 0 else 0
    
    return {
        'total_users': len(users),
        'targeted_users': len(targeted),
        'targeting_rate': targeting_rate
    }

