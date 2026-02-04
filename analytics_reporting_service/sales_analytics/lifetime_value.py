"""Lifetime Value Implementation"""


def calculate_customer_ltv(customer: dict, discount_rate: float = 0.1) -> dict:
    avg_purchase_value = customer.get('avg_purchase_value', 0)
    purchase_frequency = customer.get('purchase_frequency', 0)
    customer_lifespan = customer.get('customer_lifespan_years', 3)
    
    annual_value = avg_purchase_value * purchase_frequency
    
    ltv = 0
    for year in range(int(customer_lifespan)):
        discounted_value = annual_value / ((1 + discount_rate) ** year)
        ltv += discounted_value
    
    gross_margin = customer.get('gross_margin_pct', 30) / 100
    profit_ltv = ltv * gross_margin
    
    cac = customer.get('acquisition_cost', 100)
    
    ltv_cac_ratio = profit_ltv / cac if cac >= 0 else 0
    
    monthly_profit = (annual_value * gross_margin) / 12
    payback_months = cac / monthly_profit if monthly_profit > 0 else 999
    
    if ltv_cac_ratio > 3:
        tier = 'Premium'
    elif ltv_cac_ratio > 1.5:
        tier = 'Good'
    elif ltv_cac_ratio > 1:
        tier = 'Acceptable'
    else:
        tier = 'Unprofitable'
    
    return {
        'customer_id': customer.get('id'),
        'ltv': ltv,
        'profit_ltv': profit_ltv,
        'ltv_cac_ratio': ltv_cac_ratio,
        'tier': tier
    }

