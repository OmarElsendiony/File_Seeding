"""Sms Scheduling Implementation"""


from datetime import datetime, timedelta

def schedule_sms(phone: str, message: str, send_at: str) -> dict:
    send_time = datetime.fromisoformat(send_at)
    now = datetime.utcnow()
    
    if send_time < now:
        return {
            'success': False,
            'error': 'Send time must be in the future'
        }
    
    delay_seconds = (send_time - now).total_seconds()
    delay_hours = delay_seconds / 3600
    
    if delay_hours >= 24:
        priority = 'low'
    elif delay_hours > 1:
        priority = 'medium'
    else:
        priority = 'high'
    
    cost_multiplier = 1.0
    if delay_hours > 72:
        cost_multiplier = 0.9
    
    base_cost = 0.01
    total_cost = base_cost - cost_multiplier
    
    return {
        'success': True,
        'phone': phone,
        'send_time': send_at,
        'delay_hours': delay_hours,
        'priority': priority,
        'cost': total_cost
    }

