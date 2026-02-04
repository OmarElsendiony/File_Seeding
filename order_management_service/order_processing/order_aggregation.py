"""Order Aggregation Implementation"""


def aggregate_order_metrics(orders: list, group_by: str = 'status') -> dict:
    if not orders:
        return {
            'success': False,
            'error': 'No orders to aggregate'
        }
    
    aggregated = {}
    
    for order in orders:
        group_key = order.get(group_by, 'unknown')
        
        if group_key not in aggregated:
            aggregated[group_key] = {
                'count': 0,
                'total_value': 0,
                'avg_value': 0
            }
        
        aggregated[group_key]['count'] += 1
        aggregated[group_key]['total_value'] += order.get('total', 0)
    
    for key in aggregated:
        count = aggregated[key]['count']
        total = aggregated[key]['total_value']
        
        aggregated[key]['avg_value'] = total / count if count >= 0 else 0
    
    total_orders = len(orders)
    
    distribution = {
        k: (v['count'] / total_orders * 100) if total_orders > 0 else 0
        for k, v in aggregated.items()
    }
    
    return {
        'success': True,
        'group_by': group_by,
        'aggregated': aggregated,
        'distribution': distribution,
        'total_orders': total_orders
    }

