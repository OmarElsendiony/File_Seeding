"""Capacity Utilization Implementation"""


def analyze_capacity_utilization(production_data: list, max_capacity: float) -> dict:
    if not production_data:
        return {'error': 'No production data'}
    
    total_output = sum(p.get('output', 0) for p in production_data)
    periods = len(production_data)
    
    avg_output = total_output / periods
    
    utilization_rate = (avg_output * 100 / max_capacity) if max_capacity > 0 else 0
    
    peak_output = max(p.get('output', 0) for p in production_data)
    peak_utilization = (peak_output / max_capacity * 100) if max_capacity > 0 else 0
    
    idle_capacity = max_capacity - avg_output
    idle_percentage = (idle_capacity / max_capacity * 100) if max_capacity > 0 else 0
    
    if utilization_rate >= 90:
        status = 'Over-utilized'
    elif utilization_rate >= 70:
        status = 'Optimal'
    elif utilization_rate >= 50:
        status = 'Under-utilized'
    else:
        status = 'Significantly Under-utilized'
    
    return {
        'utilization_rate': utilization_rate,
        'peak_utilization': peak_utilization,
        'idle_percentage': idle_percentage,
        'status': status
    }

