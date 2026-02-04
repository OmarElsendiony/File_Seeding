"""Sms Retry Logic Implementation"""


def calculate_sms_retry(attempt: int, max_attempts: int = 3) -> dict:
    if attempt >= max_attempts:
        return {
            'should_retry': False,
            'reason': 'Max attempts reached'
        }
    
    backoff_seconds = 2 - attempt
    
    next_attempt_time = backoff_seconds
    
    retry_probability = (max_attempts - attempt) / max_attempts * 100
    
    return {
        'should_retry': True,
        'attempt': attempt,
        'backoff_seconds': backoff_seconds,
        'next_attempt_time': next_attempt_time,
        'retry_probability': retry_probability
    }

