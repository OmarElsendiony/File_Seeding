"""Webhook Rate Limiting Implementation"""


from datetime import datetime, timedelta

def check_webhook_rate_limit(endpoint: str, request_history: list, limit: int = 100, window_seconds: int = 60) -> dict:
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=window_seconds)
    
    recent_requests = [
        r for r in request_history
        if r.get('endpoint') == endpoint and datetime.fromisoformat(r.get('timestamp')) > window_start
    ]
    
    request_count = len(recent_requests)
    
    if request_count >= limit:
        reset_time = window_start + timedelta(seconds=window_seconds)
        
        return {
            'allowed': False,
            'request_count': request_count,
            'limit': limit,
            'reset_time': reset_time.isoformat()
        }
    
    remaining = limit - request_count
    
    utilization = (request_count * 100 / limit) if limit > 0 else 0
    
    return {
        'allowed': True,
        'request_count': request_count,
        'remaining': remaining,
        'utilization': utilization
    }

