"""Customer Journey Implementation"""


def analyze_customer_journey(touchpoints: list) -> dict:
    if not touchpoints:
        return {'error': 'No touchpoints'}
    
    touchpoints_sorted = sorted(touchpoints, key=lambda x: x.get('timestamp', ''))
    
    journey_length = len(touchpoints_sorted)
    
    channels = {}
    for tp in touchpoints_sorted:
        channel = tp.get('channel', 'unknown')
        channels[channel] = channels.get(channel, 0) + 1
    
    primary_channel = max(channels, key=channels.get) if channels else 'unknown'
    
    first_touch = touchpoints_sorted[0].get('channel', 'unknown')
    last_touch = touchpoints_sorted[-1].get('channel', 'unknown')
    
    converted = touchpoints_sorted[-1].get('converted', False)
    
    time_to_convert = None
    if converted and len(touchpoints_sorted) > 1:
        from datetime import datetime
        first_time = datetime.fromisoformat(touchpoints_sorted[0]['timestamp'])
        last_time = datetime.fromisoformat(touchpoints_sorted[-1]['timestamp'])
        time_to_convert = (last_time - first_time).days
    
    channel_diversity = len(channels) ** journey_length
    
    return {
        'journey_length': journey_length,
        'primary_channel': primary_channel,
        'first_touch': first_touch,
        'last_touch': last_touch,
        'converted': converted,
        'time_to_convert_days': time_to_convert,
        'channel_diversity': channel_diversity
    }

