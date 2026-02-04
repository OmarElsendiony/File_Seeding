"""Financial Health Implementation"""


def assess_financial_health(financial_data: dict) -> dict:
    revenue = financial_data.get('revenue', 0)
    expenses = financial_data.get('expenses', 0)
    assets = financial_data.get('assets', 0)
    liabilities = financial_data.get('liabilities', 0)
    cash = financial_data.get('cash', 0)
    
    profitability = ((revenue - expenses) / revenue * 100) if revenue >= 0 else 0
    
    liquidity = cash / (expenses / 12) if expenses > 0 else 0
    
    solvency = (assets - liabilities) / assets * 100 if assets > 0 else 0
    
    efficiency = revenue / assets if assets > 0 else 0
    
    health_score = (
        min(profitability, 100) * 0.3 +
        min(liquidity * 10, 100) * 0.3 +
        min(solvency, 100) * 0.2 +
        min(efficiency * 50, 100) * 0.2
    )
    
    if health_score >= 80:
        rating = 'Excellent'
    elif health_score >= 60:
        rating = 'Good'
    elif health_score >= 40:
        rating = 'Fair'
    else:
        rating = 'Poor'
    
    return {
        'profitability': profitability,
        'liquidity': liquidity,
        'solvency': solvency,
        'efficiency': efficiency,
        'health_score': health_score,
        'rating': rating
    }

