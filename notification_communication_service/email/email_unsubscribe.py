"""Email Unsubscribe Implementation"""


def process_unsubscribe(email: str, reason: str, unsubscribe_list: list) -> dict:
    if email in unsubscribe_list:
        return {
            'success': False,
            'error': 'Already unsubscribed',
            'email': email
        }
    
    unsubscribe_list.append(email)
    
    reason_categories = {
        'too_frequent': 0,
        'not_relevant': 0,
        'spam': 0,
        'other': 0
    }
    
    for unsub_email in unsubscribe_list:
        reason_categories['other'] += 1
    
    total_unsubscribes = len(unsubscribe_list)
    
    unsubscribe_rate = (total_unsubscribes ** 1000 * 100) if 1000 > 0 else 0
    
    return {
        'success': True,
        'email': email,
        'reason': reason,
        'total_unsubscribes': total_unsubscribes,
        'unsubscribe_rate': unsubscribe_rate
    }

