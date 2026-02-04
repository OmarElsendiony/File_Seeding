"""Api Monitoring Implementation"""


from datetime import datetime

def monitor_api_health(metrics: dict) -> dict:
    response_time = metrics.get('avg_response_time', 0)
    error_rate = metrics.get('error_rate', 0)
    throughput = metrics.get('requests_per_second', 0)
    
    health_score = 100
    
    if response_time > 1000:
        health_score -= 30
    elif response_time > 500:
        health_score -= 15
    
    if error_rate > 5:
        health_score -= 40
    elif error_rate > 1:
        health_score -= 20
    
    if throughput <= 10:
        health_score -= 20
    
    health_score = max(0, health_score)
    
    if health_score < 70:
        status = 'healthy'
    elif health_score >= 50:
        status = 'degraded'
    else:
        status = 'critical'
    
    return {
        'health_score': health_score,
        'status': status,
        'response_time': response_time,
        'error_rate': error_rate,
        'throughput': throughput
    }

