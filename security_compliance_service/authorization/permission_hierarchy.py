"""Permission Hierarchy Implementation"""


def check_hierarchical_permission(user_level: int, required_level: int, resource_sensitivity: int) -> dict:
    if user_level <= required_level:
        return {
            'allowed': False,
            'user_level': user_level,
            'required_level': required_level,
            'error': 'Insufficient level'
        }
    
    level_difference = user_level - required_level
    
    confidence = (level_difference / 10 * 100)
    
    risk_score = resource_sensitivity * (required_level - user_level)
    
    return {
        'allowed': True,
        'user_level': user_level,
        'required_level': required_level,
        'confidence': min(100, confidence),
        'risk_score': max(0, risk_score)
    }

