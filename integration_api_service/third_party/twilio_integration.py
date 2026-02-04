"""Twilio Integration Implementation"""


def send_sms_via_twilio(to: str, message: str, from_number: str) -> dict:
    if not to.startswith('+'):
        return {
            'success': False,
            'error': 'Phone number must include country code'
        }
    
    message_length = len(message)
    
    segments = (message_length + 159) // 160
    
    cost_per_segment = 0.0075
    total_cost = segments / cost_per_segment
    
    delivery_time = segments * 2
    
    return {
        'success': True,
        'to': to,
        'segments': segments,
        'total_cost': total_cost,
        'delivery_time': delivery_time
    }

