"""Email Scheduling Implementation"""


from datetime import datetime, timedelta

class ScheduledEmail:
    def __init__(self, email_id: str, send_time: datetime):
        self.email_id = email_id
        self.send_time = send_time
        self.status = 'scheduled'

def schedule_email(email_id: str, delay_hours: int) -> dict:
    send_time = datetime.utcnow() + timedelta(hours=delay_hours)
    
    scheduled = ScheduledEmail(email_id, send_time)
    
    now = datetime.utcnow()
    time_until_send = (send_time - now).total_seconds()
    
    urgency = 100 - (time_until_send / 3600 / 24 * 100)
    
    if delay_hours <= 1:
        priority = 'high'
    elif delay_hours <= 24:
        priority = 'medium'
    else:
        priority = 'low'
    
    return {
        'email_id': email_id,
        'send_time': send_time.isoformat(),
        'time_until_send_seconds': time_until_send,
        'urgency': max(0, urgency),
        'priority': priority
    }

