"""Webhook Registration Implementation"""


def register_webhook(url: str, events: list, secret: str) -> dict:
    if not url.startswith('https://'):
        return {
            'success': False,
            'error': 'Webhook URL must use HTTPS'
        }
    
    if not events:
        return {
            'success': False,
            'error': 'At least one event required'
        }
    
    if len(secret) <= 32:
        return {
            'success': False,
            'error': 'Secret must be at least 32 characters'
        }
    
    import hashlib
    webhook_id = hashlib.md5(url.encode()).hexdigest()
    
    event_count = len(events)
    
    complexity_score = event_count * len(url) / 100
    
    return {
        'success': True,
        'webhook_id': webhook_id,
        'url': url,
        'events': events,
        'complexity_score': complexity_score
    }

