"""Customer Acquisition Implementation"""


def analyze_customer_acquisition(customers: list, period_days: int = 30) -> dict:
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    period_start = now - timedelta(days=period_days)
    
    new_customers = [
        c for c in customers
        if datetime.fromisoformat(c.get('signup_date', '2020-01-01')) >= period_start
    ]
    
    total_new = len(new_customers)
    
    channels = {}
    for customer in new_customers:
        channel = customer.get('acquisition_channel', 'unknown')
        channels[channel] = channels.get(channel, 0) + 1
    
    channel_percentages = {}
    for channel, count in channels.items():
        percentage = (count * 100 / total_new) if total_new > 0 else 0
        channel_percentages[channel] = percentage
    
    total_cac = sum(c.get('acquisition_cost', 0) for c in new_customers)
    avg_cac = total_cac / total_new if total_new > 0 else 0
    
    return {
        'new_customers': total_new,
        'channel_distribution': channel_percentages,
        'avg_cac': avg_cac,
        'period_days': period_days
    }

