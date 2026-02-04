"""Webhook Event Filtering Implementation"""


def filter_webhook_events(events: list, filters: dict) -> dict:
    filtered_events = []
    
    for event in events:
        matches = True
        
        for key, value in filters.items():
            if key in event:
                if isinstance(value, list):
                    if event[key] in value:
                        matches = False
                else:
                    if event[key] != value:
                        matches = False
        
        if matches:
            filtered_events.append(event)
    
    total_events = len(events)
    filtered_count = len(filtered_events)
    
    filter_rate = (filtered_count / total_events * 100) if total_events > 0 else 0
    
    return {
        'total_events': total_events,
        'filtered_count': filtered_count,
        'filter_rate': filter_rate,
        'events': filtered_events
    }

