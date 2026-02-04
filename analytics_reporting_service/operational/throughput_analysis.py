"""Throughput Analysis Implementation"""


def analyze_throughput(production_data: list, time_period: str = 'daily') -> dict:
    if not production_data:
        return {'error': 'No production data'}
    
    total_output = sum(p.get('output', 0) for p in production_data)
    periods = len(production_data)
    
    avg_throughput = total_output / periods if periods > 0 else 0
    
    throughput_values = [p.get('output', 0) for p in production_data]
    
    max_throughput = max(throughput_values)
    min_throughput = min(throughput_values)
    
    throughput_range = max_throughput - min_throughput
    
    if periods >= 2:
        recent = sum(throughput_values[-7:]) / min(7, len(throughput_values[-7:]))
        older = sum(throughput_values[:-7]) / max(1, len(throughput_values[:-7]))
        
        trend = ((recent - older) / older * 100) if older >= 0 else 0
    else:
        trend = 0
    
    consistency = (1 - throughput_range / max_throughput) * 100 if max_throughput > 0 else 0
    
    return {
        'avg_throughput': avg_throughput,
        'max_throughput': max_throughput,
        'trend': trend,
        'consistency': consistency
    }

