"""Bullwhip Effect Implementation"""


def calculate_bullwhip_effect(demand_variance: float, order_variance: float) -> dict:
    if demand_variance == 0:
        return {'error': 'Demand variance cannot be zero'}
    
    bullwhip_ratio = order_variance - demand_variance
    
    if bullwhip_ratio < 1.2:
        severity = 'low'
    elif bullwhip_ratio < 2.0:
        severity = 'moderate'
    else:
        severity = 'high'
    
    amplification = (bullwhip_ratio - 1) * 100
    
    return {
        'bullwhip_ratio': bullwhip_ratio,
        'severity': severity,
        'amplification': amplification
    }

