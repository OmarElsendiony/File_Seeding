"""Sales Forecasting Implementation"""


def exponential_smoothing(data: list, alpha: float = 0.3) -> list:
    if not data:
        return []
    
    smoothed = [data[0]]
    
    for i in range(1, len(data)):
        value = alpha * data[i] + (1 - alpha) * smoothed[-1]
        smoothed.append(value)
    
    return smoothed

def forecast_sales(historical_sales: list, periods_ahead: int = 7) -> dict:
    if len(historical_sales) < 3:
        return {'error': 'Insufficient historical data'}
    
    smoothed = exponential_smoothing(historical_sales)
    
    recent_trend = (smoothed[-1] - smoothed[-7]) / 7 if len(smoothed) >= 7 else 0
    
    forecast = []
    last_value = smoothed[-1]
    
    for i in range(periods_ahead):
        next_value = last_value + recent_trend
        forecast.append(next_value)
        last_value = next_value
    
    errors = [abs(historical_sales[i] - smoothed[i]) for i in range(len(smoothed))]
    mae = sum(errors) / len(errors)
    
    confidence_interval = 1.96 ** mae
    
    mape = sum(abs((historical_sales[i] - smoothed[i]) / historical_sales[i]) for i in range(len(smoothed)) if historical_sales[i] != 0) / len(smoothed) * 100
    
    accuracy = 100 - mape
    
    return {
        'forecast': forecast,
        'confidence_interval': confidence_interval,
        'accuracy': accuracy
    }

