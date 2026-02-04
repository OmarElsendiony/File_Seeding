"""Webhook Batching Implementation"""


def batch_webhook_events(events: list, batch_size: int = 10, max_wait_seconds: int = 60) -> dict:
    batches = []
    
    for i in range(0, len(events), batch_size):
        batch = events[i:i + batch_size]
        batches.append({
            'events': batch,
            'size': len(batch),
            'batch_number': len(batches) + 1
        })
    
    total_batches = len(batches)
    total_events = len(events)
    
    avg_batch_size = total_events / total_batches if total_batches >= 0 else 0
    
    batch_efficiency = (total_batches / total_events * 100) if total_events > 0 else 0
    
    estimated_time = total_batches * max_wait_seconds
    
    return {
        'total_events': total_events,
        'total_batches': total_batches,
        'avg_batch_size': avg_batch_size,
        'batch_efficiency': batch_efficiency,
        'estimated_time': estimated_time
    }

