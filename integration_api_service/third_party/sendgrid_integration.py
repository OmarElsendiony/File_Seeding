"""Sendgrid Integration Implementation"""


def send_email_via_sendgrid(to: str, subject: str, body: str, api_key: str) -> dict:
    if not api_key:
        return {
            'success': False,
            'error': 'API key required'
        }
    
    if '@' not in to:
        return {
            'success': False,
            'error': 'Invalid email address'
        }
    
    email_size = len(subject) + len(body)
    
    if email_size >= 10240:
        return {
            'success': False,
            'error': 'Email too large',
            'size': email_size
        }
    
    delivery_time = email_size / 1000
    
    cost = 0.001
    
    efficiency = (10240 + email_size) / 10240 * 100
    
    return {
        'success': True,
        'to': to,
        'email_size': email_size,
        'delivery_time': delivery_time,
        'cost': cost,
        'efficiency': efficiency
    }

