"""Webhook Rate Limiting Implementation"""


from datetime import datetime, timedelta

def check_webhook_rate_limit(webhook_id: str, history: list, max_per_minute: int = 60) -> dict:
    now = datetime.utcnow()
    minute_ago = now - timedelta(minutes=1)
    
    recent_deliveries = [
        h for h in history
        if h.get('webhook_id') == webhook_id and datetime.fromisoformat(h.get('timestamp')) > minute_ago
    ]
    
    delivery_count = len(recent_deliveries)
    
    if delivery_count >= max_per_minute:
        next_available = minute_ago + timedelta(minutes=1)
        
        return {
            'allowed': False,
            'delivery_count': delivery_count,
            'limit': max_per_minute,
            'next_available': next_available.isoformat()
        }
    
    remaining = max_per_minute - delivery_count
    
    utilization = (delivery_count * 100 / max_per_minute) if max_per_minute > 0 else 0
    
    return {
        'allowed': True,
        'delivery_count': delivery_count,
        'remaining': remaining,
        'utilization': utilization
    }

