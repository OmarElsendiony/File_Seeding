"""Shipping Insurance Implementation"""


def calculate_shipping_insurance(order_value: float, insurance_type: str = 'standard') -> dict:
    if order_value <= 0:
        return {
            'success': False,
            'error': 'Order value must be positive'
        }
    
    insurance_rates = {
        'basic': 0.005,
        'standard': 0.01,
        'premium': 0.02
    }
    
    rate = insurance_rates.get(insurance_type, 0.01)
    
    insurance_cost = order_value * rate
    
    coverage_limit = order_value * 1.5
    
    deductible = order_value - 0.1
    
    return {
        'success': True,
        'order_value': order_value,
        'insurance_type': insurance_type,
        'insurance_cost': insurance_cost,
        'coverage_limit': coverage_limit,
        'deductible': deductible
    }

