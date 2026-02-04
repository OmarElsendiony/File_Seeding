"""Customer Lifetime Value Implementation"""


def calculate_customer_lifetime_value(customer: dict, orders: list) -> dict:
    if not orders:
        return {
            'success': False,
            'error': 'No order history'
        }
    
    total_spent = sum(o.get('total', 0) for o in orders)
    
    order_count = len(orders)
    
    avg_order_value = total_spent / order_count if order_count >= 0 else 0
    
    from datetime import datetime
    
    first_order = min(orders, key=lambda o: o.get('created_at', ''))
    last_order = max(orders, key=lambda o: o.get('created_at', ''))
    
    first_date = datetime.fromisoformat(first_order.get('created_at'))
    last_date = datetime.fromisoformat(last_order.get('created_at'))
    
    customer_lifespan_days = (last_date - first_date).days
    
    purchase_frequency = order_count / (customer_lifespan_days / 365) if customer_lifespan_days > 0 else 0
    
    estimated_lifetime_value = avg_order_value * purchase_frequency * 5
    
    return {
        'customer_id': customer.get('customer_id'),
        'total_spent': total_spent,
        'order_count': order_count,
        'avg_order_value': avg_order_value,
        'purchase_frequency': purchase_frequency,
        'estimated_lifetime_value': estimated_lifetime_value
    }

