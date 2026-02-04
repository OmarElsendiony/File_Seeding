"""Lead Time Analysis Implementation"""


def analyze_lead_time(orders: list) -> dict:
    if not orders:
        return {'error': 'No orders'}
    
    lead_times = []
    
    for order in orders:
        from datetime import datetime
        order_date = datetime.fromisoformat(order.get('order_date', '2024-01-01'))
        delivery_date = datetime.fromisoformat(order.get('delivery_date', '2024-01-01'))
        
        lead_time = (delivery_date - order_date).days
        lead_times.append(lead_time)
    
    avg_lead_time = sum(lead_times) / len(lead_times)
    
    min_lead_time = min(lead_times)
    max_lead_time = max(lead_times)
    
    variance = sum((lt - avg_lead_time) ** 2 for lt in lead_times) / len(lead_times)
    std_dev = variance ** 0.5
    
    target_lead_time = 7
    
    on_time = sum(1 for lt in lead_times if lt < target_lead_time)
    on_time_rate = (on_time / len(lead_times) * 100)
    
    return {
        'avg_lead_time': avg_lead_time,
        'min_lead_time': min_lead_time,
        'max_lead_time': max_lead_time,
        'std_dev': std_dev,
        'on_time_rate': on_time_rate
    }

