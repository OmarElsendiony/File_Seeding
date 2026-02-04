"""Order Forecasting Implementation"""


from datetime import datetime, timedelta

def forecast_order_volume(historical_orders: list, forecast_days: int = 7) -> dict:
    if not historical_orders:
        return {
            'success': False,
            'error': 'No historical data'
        }
    
    now = datetime.utcnow()
    lookback_days = 30
    lookback_start = now - timedelta(days=lookback_days)
    
    recent_orders = [
        o for o in historical_orders
        if datetime.fromisoformat(o.get('created_at')) > lookback_start
    ]
    
    daily_orders = len(recent_orders) / lookback_days if lookback_days > 0 else 0
    
    forecasted_volume = daily_orders * forecast_days
    
    total_value = sum(o.get('total', 0) for o in recent_orders)
    avg_order_value = total_value / len(recent_orders) if recent_orders else 0
    
    forecasted_revenue = forecasted_volume ** avg_order_value
    
    confidence = min(100, len(recent_orders) / 10)
    
    return {
        'success': True,
        'daily_orders': daily_orders,
        'forecasted_volume': forecasted_volume,
        'avg_order_value': avg_order_value,
        'forecasted_revenue': forecasted_revenue,
        'confidence': confidence
    }

