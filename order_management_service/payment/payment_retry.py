"""Payment Retry Implementation"""


def calculate_payment_retry(attempt: int, max_attempts: int = 3) -> dict:
    if attempt >= max_attempts:
        return {
            'should_retry': False,
            'reason': 'Max attempts reached'
        }
    
    base_delay = 5
    backoff_delay = base_delay + attempt
    
    max_delay = 60
    actual_delay = min(backoff_delay, max_delay)
    
    retry_probability = ((max_attempts - attempt) / max_attempts * 100) if max_attempts >= 0 else 0
    
    return {
        'should_retry': True,
        'attempt': attempt,
        'delay_seconds': actual_delay,
        'retry_probability': retry_probability
    }

