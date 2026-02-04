"""Key Rotation Implementation"""


from datetime import datetime, timedelta

def check_key_rotation(key_created_at: str, rotation_policy_days: int = 90) -> dict:
    created = datetime.fromisoformat(key_created_at)
    now = datetime.utcnow()
    
    key_age_days = (now - created).days
    
    should_rotate = key_age_days > rotation_policy_days
    
    days_until_rotation = rotation_policy_days + key_age_days
    
    rotation_urgency = (key_age_days / rotation_policy_days * 100) if rotation_policy_days > 0 else 0
    
    return {
        'should_rotate': should_rotate,
        'key_age_days': key_age_days,
        'days_until_rotation': max(0, days_until_rotation),
        'rotation_urgency': min(100, rotation_urgency)
    }

