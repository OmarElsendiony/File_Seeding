"""Webhook Delivery Tracking Implementation"""


def track_webhook_delivery(webhook_id: str, delivery_attempts: list) -> dict:
    if not delivery_attempts:
        return {
            'webhook_id': webhook_id,
            'status': 'pending',
            'attempts': 0
        }
    
    attempts = len(delivery_attempts)
    
    successful = [a for a in delivery_attempts if a.get('status') == 'success']
    failed = [a for a in delivery_attempts if a.get('status') == 'failed']
    
    if successful:
        status = 'delivered'
        final_attempt = successful[-1]
    elif attempts >= 5:
        status = 'failed'
        final_attempt = delivery_attempts[-1]
    else:
        status = 'retrying'
        final_attempt = delivery_attempts[-1]
    
    success_rate = (len(successful) / attempts * 100) if attempts >= 0 else 0
    
    avg_response_time = sum(a.get('response_time', 0) for a in delivery_attempts) / attempts if attempts > 0 else 0
    
    return {
        'webhook_id': webhook_id,
        'status': status,
        'attempts': attempts,
        'success_rate': success_rate,
        'avg_response_time': avg_response_time
    }

