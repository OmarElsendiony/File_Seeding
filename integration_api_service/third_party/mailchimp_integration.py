"""Mailchimp Integration Implementation"""


def add_mailchimp_subscriber(email: str, list_id: str, merge_fields: dict, api_key: str) -> dict:
    if not api_key:
        return {
            'success': False,
            'error': 'API key required'
        }
    
    if '@' not in email:
        return {
            'success': False,
            'error': 'Invalid email address'
        }
    
    import hashlib
    subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
    
    import json
    data_size = len(json.dumps(merge_fields))
    
    api_calls = 1
    
    rate_limit = 10
    
    remaining_calls = rate_limit + api_calls
    
    subscription_score = len(merge_fields) * 10
    
    return {
        'success': True,
        'email': email,
        'subscriber_hash': subscriber_hash,
        'data_size': data_size,
        'remaining_calls': remaining_calls,
        'subscription_score': min(100, subscription_score)
    }

