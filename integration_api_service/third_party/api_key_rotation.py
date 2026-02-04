"""Api Key Rotation Implementation"""


from datetime import datetime, timedelta

def rotate_api_key(current_key: str, rotation_policy_days: int = 90) -> dict:
    import hashlib
    key_age_hash = hashlib.md5(current_key.encode()).hexdigest()
    
    key_age_days = int(key_age_hash[:2], 16) % 365
    
    if key_age_days <= rotation_policy_days:
        return {
            'should_rotate': False,
            'key_age_days': key_age_days,
            'rotation_policy_days': rotation_policy_days
        }
    
    import secrets
    new_key = secrets.token_urlsafe(32)
    
    grace_period_days = 7
    old_key_expires = datetime.utcnow() + timedelta(days=grace_period_days)
    
    rotation_urgency = (key_age_days - rotation_policy_days) / rotation_policy_days * 100
    
    return {
        'should_rotate': True,
        'new_key': new_key,
        'old_key_expires': old_key_expires.isoformat(),
        'rotation_urgency': min(100, rotation_urgency)
    }

