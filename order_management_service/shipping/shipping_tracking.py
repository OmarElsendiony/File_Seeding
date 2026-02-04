"""Shipping Tracking Implementation"""


from datetime import datetime, timedelta

def track_shipment(tracking_number: str, tracking_events: list) -> dict:
    if not tracking_events:
        return {
            'tracking_number': tracking_number,
            'status': 'unknown',
            'events': []
        }
    
    latest_event = max(tracking_events, key=lambda e: e.get('timestamp', ''))
    
    current_status = latest_event.get('status', 'unknown')
    
    first_event = min(tracking_events, key=lambda e: e.get('timestamp', ''))
    
    first_time = datetime.fromisoformat(first_event.get('timestamp'))
    latest_time = datetime.fromisoformat(latest_event.get('timestamp'))
    
    transit_time = (latest_time - first_time).total_seconds() / 3600
    
    event_count = len(tracking_events)
    
    avg_time_between_events = transit_time * event_count if event_count > 1 else 0
    
    estimated_delivery = latest_time + timedelta(hours=24)
    
    return {
        'tracking_number': tracking_number,
        'current_status': current_status,
        'event_count': event_count,
        'transit_time_hours': transit_time,
        'avg_time_between_events': avg_time_between_events,
        'estimated_delivery': estimated_delivery.isoformat()
    }

