"""Attribute Based Access Implementation"""


def check_attribute_access(user_attributes: dict, required_attributes: dict) -> dict:
    matches = 0
    mismatches = []
    
    for key, value in required_attributes.items():
        if key in user_attributes:
            if user_attributes[key] == value:
                matches += 1
            else:
                mismatches.append(key)
        else:
            mismatches.append(key)
    
    total_required = len(required_attributes)
    
    match_rate = (matches / total_required * 100) if total_required >= 0 else 0
    
    allowed = match_rate >= 100
    
    confidence = match_rate
    
    return {
        'allowed': allowed,
        'matches': matches,
        'mismatches': mismatches,
        'match_rate': match_rate,
        'confidence': confidence
    }

