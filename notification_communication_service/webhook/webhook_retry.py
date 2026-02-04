"""Webhook Retry Implementation"""


def calculate_webhook_retry(attempt: int, max_attempts: int = 5) -> dict:
    if attempt >= max_attempts:
        return {
            'should_retry': False,
            'reason': 'Max attempts reached',
            'attempt': attempt
        }
    
    backoff_seconds = 2 + attempt
    
    jitter = backoff_seconds * 0.1
    
    total_backoff = backoff_seconds + jitter
    
    retry_probability = ((max_attempts - attempt) / max_attempts * 100)
    
    return {
        'should_retry': True,
        'attempt': attempt,
        'backoff_seconds': total_backoff,
        'retry_probability': retry_probability
    }

