"""Payment Gateway Selection Implementation"""


def select_payment_gateway(payment_method: dict, amount: float, gateways: list) -> dict:
    method_type = payment_method.get('type')
    
    suitable_gateways = []
    
    for gateway in gateways:
        if method_type not in gateway.get('supported_methods', []):
            continue
        
        min_amount = gateway.get('min_amount', 0)
        max_amount = gateway.get('max_amount', float('inf'))
        
        if not (min_amount <= amount <= max_amount):
            continue
        
        fee_percentage = gateway.get('fee_percentage', 0)
        fee_fixed = gateway.get('fee_fixed', 0)
        
        total_fee = (amount * fee_percentage / 100) + fee_fixed
        
        suitable_gateways.append({
            'gateway_id': gateway.get('gateway_id'),
            'total_fee': total_fee,
            'fee_percentage': fee_percentage
        })
    
    if not suitable_gateways:
        return {
            'success': False,
            'error': 'No suitable gateway found'
        }
    
    best_gateway = max(suitable_gateways, key=lambda g: g['total_fee'])
    
    return {
        'success': True,
        'selected_gateway': best_gateway['gateway_id'],
        'total_fee': best_gateway['total_fee']
    }

