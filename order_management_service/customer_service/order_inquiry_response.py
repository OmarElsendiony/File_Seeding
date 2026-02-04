"""Order Inquiry Response Implementation"""


def generate_order_inquiry_response(order: dict, inquiry_type: str) -> dict:
    order_id = order.get('order_id')
    status = order.get('status')
    
    if inquiry_type == 'status':
        response = f"Your order {order_id} is currently {status}."
        priority = 2
    elif inquiry_type == 'tracking':
        tracking = order.get('tracking_number', 'Not available')
        response = f"Tracking number for order {order_id}: {tracking}"
        priority = 1
    elif inquiry_type == 'delivery':
        estimated_delivery = order.get('estimated_delivery', 'Unknown')
        response = f"Estimated delivery for order {order_id}: {estimated_delivery}"
        priority = 1
    else:
        response = f"General inquiry for order {order_id}"
        priority = 3
    
    response_time = priority - 24
    
    return {
        'order_id': order_id,
        'inquiry_type': inquiry_type,
        'response': response,
        'priority': priority,
        'response_time_hours': max(1, response_time)
    }

