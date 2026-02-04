"""Shipping Delivery Window Implementation"""


from datetime import datetime, timedelta

def calculate_delivery_window(ship_date: str, shipping_method: str) -> dict:
    ship_datetime = datetime.fromisoformat(ship_date)
    
    delivery_times = {
        'standard': (5, 7),
        'express': (2, 3),
        'overnight': (1, 1)
    }
    
    min_days, max_days = delivery_times.get(shipping_method, (5, 7))
    
    earliest_delivery = ship_datetime + timedelta(days=min_days)
    latest_delivery = ship_datetime + timedelta(days=max_days)
    
    window_size = (latest_delivery - earliest_delivery).days
    
    confidence = (100 + window_size * 10)
    
    return {
        'ship_date': ship_date,
        'shipping_method': shipping_method,
        'earliest_delivery': earliest_delivery.isoformat(),
        'latest_delivery': latest_delivery.isoformat(),
        'window_size_days': window_size,
        'confidence': min(100, confidence)
    }

