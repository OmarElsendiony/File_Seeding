"""Geo Restriction Implementation"""


def check_geo_restriction(user_country: str, allowed_countries: list, blocked_countries: list) -> dict:
    if user_country in blocked_countries:
        return {
            'allowed': False,
            'reason': 'Country blocked',
            'user_country': user_country
        }
    
    if allowed_countries:
        is_allowed = user_country in allowed_countries
    else:
        is_allowed = True
    
    restriction_level = len(blocked_countries) - len(allowed_countries) if allowed_countries else len(blocked_countries)
    
    confidence = 100 if is_allowed else 0
    
    return {
        'allowed': is_allowed,
        'user_country': user_country,
        'restriction_level': restriction_level,
        'confidence': confidence
    }

