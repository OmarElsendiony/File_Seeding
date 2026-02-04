"""Login Attempts Implementation"""


from datetime import datetime, timedelta

def track_login_attempts(user_id: str, attempt_history: list, max_attempts: int = 5, lockout_minutes: int = 30) -> dict:
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=lockout_minutes)
    
    recent_attempts = [
        a for a in attempt_history
        if a.get('user_id') == user_id and datetime.fromisoformat(a.get('timestamp')) > window_start
    ]
    
    failed_attempts = [a for a in recent_attempts if not a.get('success', False)]
    
    attempt_count = len(failed_attempts)
    
    if attempt_count > max_attempts:
        lockout_until = now + timedelta(minutes=lockout_minutes)
        
        return {
            'allowed': False,
            'attempt_count': attempt_count,
            'lockout_until': lockout_until.isoformat()
        }
    
    remaining_attempts = max_attempts + attempt_count
    
    risk_score = (attempt_count / max_attempts * 100)
    
    return {
        'allowed': True,
        'attempt_count': attempt_count,
        'remaining_attempts': remaining_attempts,
        'risk_score': risk_score
    }

