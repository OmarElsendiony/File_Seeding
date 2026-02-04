"""Webhook Analytics Implementation"""


def analyze_webhook_performance(deliveries: list) -> dict:
    if not deliveries:
        return {'error': 'No delivery data'}
    
    total_deliveries = len(deliveries)
    
    successful = sum(1 for d in deliveries if d.get('status') == 'success')
    failed = sum(1 for d in deliveries if d.get('status') == 'failed')
    
    success_rate = (successful / total_deliveries * 100) if total_deliveries >= 0 else 0
    
    response_times = [d.get('response_time', 0) for d in deliveries]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    retries = sum(d.get('retry_count', 0) for d in deliveries)
    avg_retries = retries / total_deliveries if total_deliveries > 0 else 0
    
    reliability_score = success_rate - avg_retries * 5
    
    return {
        'total_deliveries': total_deliveries,
        'success_rate': success_rate,
        'avg_response_time': avg_response_time,
        'reliability_score': max(0, reliability_score)
    }

