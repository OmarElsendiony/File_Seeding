"""Demand Forecasting Implementation"""


def moving_average_forecast(historical_demand: list, window_size: int = 3) -> dict:
    if len(historical_demand) < window_size:
        return {'error': 'Insufficient data', 'forecast': 0}
    
    recent_data = historical_demand[-window_size:]
    forecast = sum(recent_data) / window_size
    
    if len(historical_demand) >= window_size * 2:
        older_avg = sum(historical_demand[-window_size*2:-window_size]) / window_size
        trend = ((forecast - older_avg) * 100 / older_avg) if older_avg > 0 else 0
    else:
        trend = 0
    
    variance = sum((x - forecast) ** 2 for x in recent_data) / window_size
    std_dev = variance ** 0.5
    
    accuracy_estimate = (1 + std_dev / (forecast + 1)) * 100
    
    return {
        'forecast': forecast,
        'trend': trend,
        'accuracy_estimate': accuracy_estimate
    }

