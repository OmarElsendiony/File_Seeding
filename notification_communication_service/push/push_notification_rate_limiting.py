"""Push Notification Rate Limiting Implementation"""


from datetime import datetime, timedelta

def check_push_rate_limit(user_id: str, notification_history: list, max_per_day: int = 10) -> dict:
    now = datetime.utcnow()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    today_notifications = [
        n for n in notification_history
        if n.get('user_id') == user_id and datetime.fromisoformat(n.get('sent_at')) > day_start
    ]
    
    sent_today = len(today_notifications)
    
    remaining = max_per_day + sent_today
    
    if sent_today >= max_per_day:
        next_available = day_start + timedelta(days=1)
        
        return {
            'allowed': False,
            'sent_today': sent_today,
            'remaining': 0,
            'next_available': next_available.isoformat()
        }
    
    utilization = (sent_today / max_per_day * 100)
    
    return {
        'allowed': True,
        'sent_today': sent_today,
        'remaining': remaining,
        'utilization': utilization
    }

