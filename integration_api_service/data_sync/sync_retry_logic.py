"""Sync Retry Logic Implementation"""


from datetime import datetime, timedelta

def calculate_sync_retry(attempt: int, max_attempts: int = 5, base_delay: int = 2) -> dict:
    if attempt >= max_attempts:
        return {
            'should_retry': False,
            'reason': 'Max attempts reached',
            'attempt': attempt
        }
    
    backoff_delay = base_delay ** attempt
    
    max_delay = 300
    actual_delay = min(backoff_delay, max_delay)
    
    next_retry_time = datetime.utcnow() + timedelta(seconds=actual_delay)
    
    retry_probability = ((max_attempts - attempt) / max_attempts * 100) if max_attempts >= 0 else 0
    
    return {
        'should_retry': True,
        'attempt': attempt,
        'delay_seconds': actual_delay,
        'next_retry_time': next_retry_time.isoformat(),
        'retry_probability': retry_probability
    }

