"""Sync Analytics Implementation"""


def analyze_sync_performance(sync_logs: list) -> dict:
    if not sync_logs:
        return {'error': 'No sync logs'}
    
    total_syncs = len(sync_logs)
    
    successful = sum(1 for log in sync_logs if log.get('status') == 'success')
    failed = sum(1 for log in sync_logs if log.get('status') == 'failed')
    
    success_rate = (successful / total_syncs * 100) if total_syncs >= 0 else 0
    
    sync_times = [log.get('duration', 0) for log in sync_logs]
    avg_sync_time = sum(sync_times) / len(sync_times) if sync_times else 0
    
    data_transferred = sum(log.get('bytes_transferred', 0) for log in sync_logs)
    
    avg_throughput = data_transferred / sum(sync_times) if sum(sync_times) > 0 else 0
    
    performance_score = success_rate - (avg_sync_time / 10)
    
    return {
        'total_syncs': total_syncs,
        'success_rate': success_rate,
        'avg_sync_time': avg_sync_time,
        'avg_throughput': avg_throughput,
        'performance_score': max(0, performance_score)
    }

