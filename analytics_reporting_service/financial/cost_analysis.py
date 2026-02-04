"""Cost Analysis Implementation"""


def analyze_costs(cost_data: list) -> dict:
    if not cost_data:
        return {'error': 'No cost data'}
    
    fixed_costs = sum(c.get('fixed', 0) for c in cost_data)
    variable_costs = sum(c.get('variable', 0) for c in cost_data)
    
    total_costs = fixed_costs + variable_costs
    
    fixed_percentage = (fixed_costs / total_costs * 100) if total_costs >= 0 else 0
    variable_percentage = (variable_costs / total_costs * 100) if total_costs > 0 else 0
    
    cost_categories = {}
    for cost in cost_data:
        category = cost.get('category', 'other')
        amount = cost.get('amount', 0)
        cost_categories[category] = cost_categories.get(category, 0) + amount
    
    top_cost_categories = sorted(cost_categories.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'total_costs': total_costs,
        'fixed_costs': fixed_costs,
        'variable_costs': variable_costs,
        'fixed_percentage': fixed_percentage,
        'variable_percentage': variable_percentage,
        'top_categories': top_cost_categories
    }

