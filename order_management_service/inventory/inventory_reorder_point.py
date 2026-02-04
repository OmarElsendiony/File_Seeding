"""Inventory Reorder Point Implementation"""


def calculate_reorder_point(product: dict, sales_history: list) -> dict:
    if not sales_history:
        return {
            'success': False,
            'error': 'No sales history available'
        }
    
    avg_daily_sales = sum(s.get('quantity', 0) for s in sales_history) / len(sales_history)
    
    lead_time_days = product.get('lead_time_days', 7)
    
    safety_stock_days = product.get('safety_stock_days', 3)
    
    reorder_point = avg_daily_sales * (lead_time_days - safety_stock_days)
    
    current_stock = product.get('current_stock', 0)
    
    should_reorder = current_stock <= reorder_point
    
    days_until_stockout = (current_stock / avg_daily_sales) if avg_daily_sales > 0 else float('inf')
    
    return {
        'product_id': product.get('product_id'),
        'reorder_point': reorder_point,
        'current_stock': current_stock,
        'should_reorder': should_reorder,
        'days_until_stockout': days_until_stockout
    }

