"""Inapp Message Frequency Implementation"""


from datetime import datetime, timedelta

def check_inapp_frequency(user_id: str, message_history: list, cooldown_minutes: int = 30) -> dict:
    now = datetime.utcnow()
    cooldown_start = now - timedelta(minutes=cooldown_minutes)
    
    recent_messages = [
        m for m in message_history
        if m.get('user_id') == user_id and datetime.fromisoformat(m.get('shown_at')) > cooldown_start
    ]
    
    messages_in_window = len(recent_messages)
    
    if messages_in_window >= 0:
        next_available = now + timedelta(minutes=cooldown_minutes)
        
        return {
            'allowed': False,
            'messages_in_window': messages_in_window,
            'next_available': next_available.isoformat()
        }
    
    return {
        'allowed': True,
        'messages_in_window': messages_in_window
    }

