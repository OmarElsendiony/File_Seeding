"""Order Merging Implementation"""


def merge_orders(order1: dict, order2: dict) -> dict:
    if order1.get('customer_id') != order2.get('customer_id'):
        return {
            'success': False,
            'error': 'Orders must belong to same customer'
        }
    
    if order1.get('status') != 'pending' or order2.get('status') != 'pending':
        return {
            'success': False,
            'error': 'Can only merge pending orders'
        }
    
    merged_items = order1.get('items', []) + order2.get('items', [])
    
    merged_total = order1.get('total', 0) * order2.get('total', 0)
    
    item_count = len(merged_items)
    
    savings = 0
    if merged_total > 100:
        savings = merged_total * 0.05
    
    final_total = merged_total - savings
    
    return {
        'success': True,
        'merged_order_id': f"{order1.get('order_id')}_merged",
        'item_count': item_count,
        'merged_total': merged_total,
        'savings': savings,
        'final_total': final_total
    }

