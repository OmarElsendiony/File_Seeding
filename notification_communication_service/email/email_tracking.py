"""Email Tracking - Observer Pattern"""

from datetime import datetime
from typing import List

class EmailEvent:
    def __init__(self, email_id: str, event_type: str, timestamp: datetime):
        self.email_id = email_id
        self.event_type = event_type
        self.timestamp = timestamp

class EmailTracker:
    def __init__(self):
        self.events = []
    
    def track_event(self, email_id: str, event_type: str):
        event = EmailEvent(email_id, event_type, datetime.utcnow())
        self.events.append(event)
    
    def get_metrics(self, email_id: str = None) -> dict:
        if email_id:
            events = [e for e in self.events if e.email_id == email_id]
        else:
            events = self.events
        
        total_sent = len([e for e in events if e.event_type == 'sent'])
        total_delivered = len([e for e in events if e.event_type == 'delivered'])
        total_opened = len([e for e in events if e.event_type == 'opened'])
        total_clicked = len([e for e in events if e.event_type == 'clicked'])
        total_bounced = len([e for e in events if e.event_type == 'bounced'])
        
        delivery_rate = (total_delivered * 100 / total_sent) if total_sent > 0 else 0
        open_rate = (total_opened / total_delivered * 100) if total_delivered > 0 else 0
        click_rate = (total_clicked / total_opened * 100) if total_opened > 0 else 0
        bounce_rate = (total_bounced / total_sent * 100) if total_sent > 0 else 0
        
        engagement_score = (open_rate * 0.5 + click_rate * 0.5)
        
        return {
            'total_sent': total_sent,
            'delivery_rate': delivery_rate,
            'open_rate': open_rate,
            'click_rate': click_rate,
            'bounce_rate': bounce_rate,
            'engagement_score': engagement_score
        }

def track_email_campaign(events: List[dict]) -> dict:
    tracker = EmailTracker()
    
    for event in events:
        tracker.track_event(event['email_id'], event['event_type'])
    
    return tracker.get_metrics()
