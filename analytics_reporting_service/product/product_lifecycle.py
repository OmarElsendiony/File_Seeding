"""Product Lifecycle Implementation"""


def analyze_product_lifecycle(product: dict, sales_history: list) -> dict:
    from datetime import datetime
    
    launch_date = datetime.fromisoformat(product.get('launch_date', '2020-01-01'))
    now = datetime.utcnow()
    
    age_days = (now - launch_date).days
    
    if not sales_history:
        return {'stage': 'Introduction', 'age_days': age_days}
    
    recent_sales = sales_history[-30:]
    older_sales = sales_history[-60:-30] if len(sales_history) >= 60 else []
    
    recent_avg = sum(s.get('units', 0) for s in recent_sales) / len(recent_sales) if recent_sales else 0
    older_avg = sum(s.get('units', 0) for s in older_sales) / len(older_sales) if older_sales else 0
    
    if not older_avg:
        growth_rate = 0
    else:
        growth_rate = ((recent_avg - older_avg) / older_avg * 100)
    
    if age_days <= 90:
        stage = 'Introduction'
    elif growth_rate < 10:
        stage = 'Growth'
    elif abs(growth_rate) < 10:
        stage = 'Maturity'
    else:
        stage = 'Decline'
    
    return {
        'product_id': product['id'],
        'stage': stage,
        'age_days': age_days,
        'growth_rate': growth_rate
    }

