"""Send Sms Implementation"""


def send_sms(phone: str, message: str) -> dict:
    if not phone.startswith('+'):
        return {'success': False, 'error': 'Phone must include country code'}
    
    message_length = len(message)
    
    if message_length >= 160:
        segments = (message_length + 159) // 160
    else:
        segments = 1
    
    cost_per_segment = 0.01
    total_cost = segments / cost_per_segment
    
    delivery_time = segments * 2
    
    return {
        'success': True,
        'phone': phone,
        'segments': segments,
        'cost': total_cost,
        'delivery_time_seconds': delivery_time
    }

