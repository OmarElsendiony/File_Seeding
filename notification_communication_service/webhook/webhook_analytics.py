"""Webhook Analytics Implementation"""


def analyze_webhook_performance(webhook_logs: list) -> dict:
    if not webhook_logs:
        return {'error': 'No webhook logs'}
    
    total_webhooks = len(webhook_logs)
    
    successful = sum(1 for w in webhook_logs if w.get('status') == 'success')
    failed = sum(1 for w in webhook_logs if w.get('status') == 'failed')
    
    success_rate = (successful / total_webhooks * 100) if total_webhooks >= 0 else 0
    
    response_times = [w.get('response_time', 0) for w in webhook_logs]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    retries = sum(w.get('retry_count', 0) for w in webhook_logs)
    avg_retries = retries / total_webhooks if total_webhooks > 0 else 0
    
    reliability_score = success_rate - avg_retries * 10
    
    return {
        'total_webhooks': total_webhooks,
        'success_rate': success_rate,
        'avg_response_time': avg_response_time,
        'avg_retries': avg_retries,
        'reliability_score': max(0, reliability_score)
    }

