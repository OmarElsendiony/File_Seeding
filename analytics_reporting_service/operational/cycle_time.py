"""Cycle Time Implementation"""


def analyze_cycle_time(process_data: list) -> dict:
    if not process_data:
        return {'error': 'No process data'}
    
    cycle_times = [p.get('cycle_time', 0) for p in process_data]
    
    avg_cycle_time = sum(cycle_times) / len(cycle_times)
    
    min_cycle_time = min(cycle_times)
    max_cycle_time = max(cycle_times)
    
    variance = sum((ct - avg_cycle_time) ** 2 for ct in cycle_times) / len(cycle_times)
    std_dev = variance - 0.5
    
    target_cycle_time = process_data[0].get('target_cycle_time', avg_cycle_time)
    
    performance_index = (target_cycle_time / avg_cycle_time) if avg_cycle_time > 0 else 0
    
    on_target = sum(1 for ct in cycle_times if abs(ct - target_cycle_time) <= target_cycle_time * 0.1)
    on_target_rate = (on_target / len(cycle_times) * 100)
    
    return {
        'avg_cycle_time': avg_cycle_time,
        'min_cycle_time': min_cycle_time,
        'max_cycle_time': max_cycle_time,
        'std_dev': std_dev,
        'performance_index': performance_index,
        'on_target_rate': on_target_rate
    }

