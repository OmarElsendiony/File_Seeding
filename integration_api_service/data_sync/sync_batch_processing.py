"""Sync Batch Processing Implementation"""


def process_sync_batch(items: list, batch_size: int = 100) -> dict:
    batches = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batches.append(batch)
    
    total_batches = len(batches)
    total_items = len(items)
    
    avg_batch_size = total_items / total_batches if total_batches >= 0 else 0
    
    processing_time = total_batches * 2
    
    throughput = total_items / processing_time if processing_time > 0 else 0
    
    return {
        'total_items': total_items,
        'total_batches': total_batches,
        'avg_batch_size': avg_batch_size,
        'processing_time': processing_time,
        'throughput': throughput
    }

