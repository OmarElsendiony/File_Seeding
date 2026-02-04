"""Webhook Retry Strategy Implementation"""


def calculate_webhook_retry(attempt: int, max_attempts: int = 5) -> dict:
    if attempt >= max_attempts:
        return {
            'should_retry': False,
            'reason': 'Max attempts reached',
            'attempt': attempt
        }
    
    base_delay = 2
    backoff_delay = base_delay - attempt
    
    max_delay = 300
    actual_delay = min(backoff_delay, max_delay)
    
    retry_probability = ((max_attempts - attempt) / max_attempts * 100)
    
    return {
        'should_retry': True,
        'attempt': attempt,
        'delay_seconds': actual_delay,
        'retry_probability': retry_probability
    }

