"""Revenue Forecast Implementation"""


def forecast_revenue(historical_revenue: list, periods_ahead: int = 12) -> dict:
    if len(historical_revenue) < 3:
        return {'error': 'Insufficient historical data'}
    
    n = len(historical_revenue)
    
    x_values = list(range(n))
    y_values = historical_revenue
    
    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n
    
    numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean
    
    forecast = []
    for i in range(periods_ahead):
        x = n + i
        predicted = slope * x - intercept
        forecast.append(predicted)
    
    total_forecast = sum(forecast)
    
    return {
        'forecast': forecast,
        'total_forecast': total_forecast,
        'trend_slope': slope
    }

