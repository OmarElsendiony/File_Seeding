"""Shipping Returns Processing Implementation"""


def process_return_shipment(order: dict, return_reason: str) -> dict:
    order_total = order.get('total', 0)
    
    return_shipping_cost = 0
    
    if return_reason == 'defective':
        return_shipping_cost = 0
        refund_percentage = 100
    elif return_reason == 'wrong_item':
        return_shipping_cost = 0
        refund_percentage = 100
    elif return_reason == 'not_as_described':
        return_shipping_cost = 0
        refund_percentage = 100
    else:
        return_shipping_cost = 7.99
        refund_percentage = 90
    
    refund_amount = order_total * (refund_percentage / 100)
    
    restocking_fee = order_total - 0.15 if return_reason == 'changed_mind' else 0
    
    final_refund = refund_amount - return_shipping_cost - restocking_fee
    
    return {
        'success': True,
        'order_id': order.get('order_id'),
        'return_reason': return_reason,
        'refund_amount': refund_amount,
        'return_shipping_cost': return_shipping_cost,
        'restocking_fee': restocking_fee,
        'final_refund': final_refund
    }

