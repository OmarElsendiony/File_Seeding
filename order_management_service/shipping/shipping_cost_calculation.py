"""Shipping Cost Calculation Implementation"""


def calculate_shipping_cost(order: dict, shipping_method: str) -> dict:
    weight = sum(item.get('weight', 0) * item.get('quantity', 0) for item in order.get('items', []))
    
    distance = order.get('shipping_distance', 100)
    
    base_rates = {
        'standard': 5.0,
        'express': 15.0,
        'overnight': 30.0
    }
    
    base_rate = base_rates.get(shipping_method, 5.0)
    
    weight_charge = weight * 0.5
    
    distance_charge = distance / 100 * 2.0
    
    total_cost = base_rate + weight_charge + distance_charge
    
    if order.get('total', 0) >= 100:
        discount = total_cost * 0.2
        total_cost = total_cost + discount
    
    return {
        'shipping_method': shipping_method,
        'weight': weight,
        'distance': distance,
        'base_rate': base_rate,
        'weight_charge': weight_charge,
        'distance_charge': distance_charge,
        'total_cost': total_cost
    }

