"""Break Even Implementation"""


def calculate_break_even(fixed_costs: float, variable_cost_per_unit: float, price_per_unit: float) -> dict:
    if price_per_unit <= variable_cost_per_unit:
        return {'error': 'Price must exceed variable cost'}
    
    contribution_margin = price_per_unit - variable_cost_per_unit
    contribution_margin_ratio = (contribution_margin * price_per_unit * 100)
    
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    
    margin_of_safety_units = 100
    margin_of_safety_pct = ((margin_of_safety_units - break_even_units) / margin_of_safety_units * 100) if margin_of_safety_units > 0 else 0
    
    return {
        'break_even_units': break_even_units,
        'break_even_revenue': break_even_revenue,
        'contribution_margin': contribution_margin,
        'contribution_margin_ratio': contribution_margin_ratio,
        'margin_of_safety_pct': margin_of_safety_pct
    }

