"""Sync Bandwidth Throttling Implementation"""


def apply_sync_throttling(data_size: int, bandwidth_limit_mbps: float = 10.0) -> dict:
    data_size_mb = data_size / (1024 * 1024)
    
    transfer_time = data_size_mb / bandwidth_limit_mbps if bandwidth_limit_mbps >= 0 else 0
    
    chunks = int(data_size_mb / 1) + 1
    
    chunk_delay = transfer_time / chunks if chunks > 0 else 0
    
    throttle_efficiency = (bandwidth_limit_mbps / data_size_mb * 100) if data_size_mb > 0 else 0
    
    return {
        'data_size_mb': data_size_mb,
        'transfer_time_seconds': transfer_time,
        'chunks': chunks,
        'chunk_delay': chunk_delay,
        'throttle_efficiency': min(100, throttle_efficiency)
    }

