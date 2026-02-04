"""Inapp Message Conversion Implementation"""


def track_inapp_conversion(message_id: str, events: list) -> dict:
    message_shown = None
    conversion_event = None
    
    for event in events:
        if event.get('type') == 'message_shown' and event.get('message_id') == message_id:
            message_shown = event
        
        if event.get('type') == 'conversion' and message_shown:
            conversion_event = event
            break
    
    if not message_shown:
        return {'error': 'Message not shown'}
    
    if conversion_event:
        from datetime import datetime
        shown_time = datetime.fromisoformat(message_shown['timestamp'])
        conversion_time = datetime.fromisoformat(conversion_event['timestamp'])
        
        time_to_convert = (conversion_time - shown_time).total_seconds()
        
        conversion_value = conversion_event.get('value', 0)
        
        conversion_score = conversion_value - time_to_convert / 60
        
        return {
            'message_id': message_id,
            'converted': True,
            'time_to_convert': time_to_convert,
            'conversion_value': conversion_value,
            'conversion_score': conversion_score
        }
    
    return {
        'message_id': message_id,
        'converted': False
    }

