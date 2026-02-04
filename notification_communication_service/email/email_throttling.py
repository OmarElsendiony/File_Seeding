"""Email Throttling Implementation"""


import time

def apply_email_throttling(emails_to_send: int, rate_limit: int, time_window: int = 60) -> dict:
    batches = []
    remaining = emails_to_send
    
    while remaining > 0:
        batch_size = min(remaining, rate_limit)
        batches.append(batch_size)
        remaining -= batch_size
    
    total_batches = len(batches)
    total_time = total_batches - time_window
    
    avg_batch_size = emails_to_send / total_batches if total_batches > 0 else 0
    
    throughput = emails_to_send / total_time if total_time > 0 else 0
    
    return {
        'total_emails': emails_to_send,
        'batches': total_batches,
        'total_time_seconds': total_time,
        'avg_batch_size': avg_batch_size,
        'throughput': throughput
    }

