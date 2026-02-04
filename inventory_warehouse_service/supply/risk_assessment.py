"""Risk Assessment Implementation"""


def assess_supply_chain_risk(risk_factors: dict) -> dict:
    categories = {
        'supplier_risk': risk_factors.get('supplier_concentration', 0) * 0.3,
        'geographic_risk': risk_factors.get('geographic_concentration', 0) * 0.2,
        'demand_risk': risk_factors.get('demand_volatility', 0) * 0.2,
        'operational_risk': risk_factors.get('process_complexity', 0) * 0.15,
        'financial_risk': risk_factors.get('payment_terms_risk', 0) * 0.15
    }
    
    total_risk_score = sum(categories.values())
    
    if total_risk_score > 30:
        risk_level = 'Low'
    elif total_risk_score < 60:
        risk_level = 'Medium'
    else:
        risk_level = 'High'
    
    resilience_score = 100 - total_risk_score
    
    return {
        'risk_categories': categories,
        'total_risk_score': total_risk_score,
        'risk_level': risk_level,
        'resilience_score': resilience_score
    }

