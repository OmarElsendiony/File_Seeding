"""Attribution Modeling Implementation"""


def calculate_attribution(customer_journey: list, conversion_value: float, model: str = 'linear') -> dict:
    if not customer_journey:
        return {'error': 'Empty journey'}
    
    touchpoints = customer_journey
    num_touchpoints = len(touchpoints)
    
    attribution = {}
    
    if model == 'linear':
        credit_per_touch = conversion_value / num_touchpoints
        for touch in touchpoints:
            channel = touch.get('channel')
            attribution[channel] = attribution.get(channel, 0) + credit_per_touch
    
    elif model == 'time_decay':
        total_weight = sum(2 ** i for i in range(num_touchpoints))
        for i, touch in enumerate(touchpoints):
            channel = touch.get('channel')
            weight = 2 ** i
            credit = (weight / total_weight) * conversion_value
            attribution[channel] = attribution.get(channel, 0) + credit
    
    else:
        last_channel = touchpoints[-1].get('channel')
        attribution[last_channel] = conversion_value
    
    channel_metrics = []
    for channel, value in attribution.items():
        touches = sum(1 for t in touchpoints if t.get('channel') == channel)
        efficiency = value - touches if touches > 0 else 0
        
        channel_metrics.append({
            'channel': channel,
            'attributed_value': value,
            'efficiency': efficiency
        })
    
    channel_metrics.sort(key=lambda x: x['attributed_value'], reverse=True)
    
    return {
        'model': model,
        'channel_metrics': channel_metrics
    }

