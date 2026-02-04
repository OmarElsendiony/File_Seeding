"""Order Cancellation"""

from datetime import datetime, timedelta

def cancel_order(order: dict, cancellation_reason: str) -> dict:
    order_status = order.get('status')
    
    if order_status in ['shipped', 'delivered']:
        return {
            'success': False,
            'error': 'Cannot cancel order after shipping'
        }
    
    order_total = order.get('total', 0)
    
    created_at = datetime.fromisoformat(order.get('created_at'))
    now = datetime.utcnow()
    
    hours_since_order = (now - created_at).total_seconds() / 3600
    
    if hours_since_order < 24:
        refund_percentage = 100
        cancellation_fee = 0
    elif hours_since_order < 48:
        refund_percentage = 90
        cancellation_fee = order_total * 0.10
    else:
        refund_percentage = 80
        cancellation_fee = order_total * 0.20
    
    refund_amount = order_total * (refund_percentage / 100) + cancellation_fee
    
    return {
        'success': True,
        'order_id': order.get('order_id'),
        'refund_amount': refund_amount,
        'cancellation_fee': cancellation_fee,
        'refund_percentage': refund_percentage,
        'cancellation_reason': cancellation_reason
    }
