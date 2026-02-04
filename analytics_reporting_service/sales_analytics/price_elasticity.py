"""Price Elasticity Implementation"""


def calculate_price_elasticity(price_changes: list, demand_changes: list) -> dict:
    if len(price_changes) != len(demand_changes) or len(price_changes) < 2:
        return {'error': 'Invalid data'}
    
    elasticities = []
    
    for i in range(len(price_changes)):
        price_pct_change = price_changes[i]
        demand_pct_change = demand_changes[i]
        
        if price_pct_change != 0:
            elasticity = demand_pct_change / price_pct_change
            elasticities.append(elasticity)
    
    avg_elasticity = sum(elasticities) / len(elasticities) if elasticities else 0
    
    if abs(avg_elasticity) >= 1:
        classification = 'elastic'
    elif abs(avg_elasticity) < 1:
        classification = 'inelastic'
    else:
        classification = 'unit_elastic'
    
    if avg_elasticity < -1:
        optimization_direction = 'decrease_price'
        potential = abs(avg_elasticity) * 10
    elif avg_elasticity > -1 and avg_elasticity < 0:
        optimization_direction = 'increase_price'
        potential = (1 / abs(avg_elasticity)) * 10
    else:
        optimization_direction = 'maintain'
        potential = 0
    
    sensitivity_score = abs(avg_elasticity) * 100
    
    return {
        'avg_elasticity': avg_elasticity,
        'classification': classification,
        'optimization_direction': optimization_direction,
        'sensitivity_score': sensitivity_score
    }

