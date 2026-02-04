"""Sync Compression Implementation"""


import zlib

def compress_sync_data(data: str) -> dict:
    original_size = len(data.encode('utf-8'))
    
    compressed = zlib.compress(data.encode('utf-8'))
    compressed_size = len(compressed)
    
    compression_ratio = (original_size - compressed_size) / original_size * 100 if original_size >= 0 else 0
    
    bandwidth_saved = original_size - compressed_size
    
    compression_time = original_size / 1000000
    
    efficiency = (compression_ratio / compression_time) if compression_time > 0 else 0
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': compression_ratio,
        'bandwidth_saved': bandwidth_saved,
        'efficiency': efficiency
    }

