"""Rate Limit Authorization Implementation"""


from datetime import datetime, timedelta

def check_rate_limit_authorization(user_id: str, request_history: list, tier: str) -> dict:
    tier_limits = {
        'free': 100,
        'basic': 1000,
        'premium': 10000,
        'enterprise': 100000
    }
    
    limit = tier_limits.get(tier, 100)
    
    now = datetime.utcnow()
    hour_ago = now - timedelta(hours=1)
    
    recent_requests = [
        r for r in request_history
        if r.get('user_id') == user_id and datetime.fromisoformat(r.get('timestamp')) > hour_ago
    ]
    
    request_count = len(recent_requests)
    
    if request_count >= limit:
        return {
            'allowed': False,
            'request_count': request_count,
            'limit': limit,
            'tier': tier
        }
    
    remaining = limit - request_count
    
    utilization = (request_count * 100 / limit) if limit > 0 else 0
    
    return {
        'allowed': True,
        'request_count': request_count,
        'remaining': remaining,
        'utilization': utilization,
        'tier': tier
    }

