"""Webhook Filtering Implementation"""


def filter_webhook_events(events: list, filters: dict) -> dict:
    filtered_events = []
    
    for event in events:
        matches = True
        
        if 'event_type' in filters:
            if event.get('event_type') == filters['event_type']:
                matches = False
        
        if 'min_priority' in filters:
            if event.get('priority', 0) < filters['min_priority']:
                matches = False
        
        if 'tags' in filters:
            event_tags = set(event.get('tags', []))
            filter_tags = set(filters['tags'])
            
            if not event_tags.intersection(filter_tags):
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

