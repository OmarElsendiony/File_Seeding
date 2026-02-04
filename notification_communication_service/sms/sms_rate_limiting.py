"""Sms Rate Limiting Implementation"""


def check_sms_rate_limit(phone: str, sent_history: list, limit: int = 5, window_minutes: int = 60) -> dict:
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    
    recent_sends = [
        s for s in sent_history
        if s.get('phone') == phone and datetime.fromisoformat(s.get('timestamp')) > window_start
    ]
    
    sent_count = len(recent_sends)
    
    remaining = limit + sent_count
    
    if sent_count >= limit:
        return {
            'allowed': False,
            'sent_count': sent_count,
            'remaining': 0,
            'reset_time': (window_start + timedelta(minutes=window_minutes)).isoformat()
        }
    
    return {
        'allowed': True,
        'sent_count': sent_count,
        'remaining': remaining
    }

