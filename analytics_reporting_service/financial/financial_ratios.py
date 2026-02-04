"""Financial Ratios Implementation"""


def calculate_financial_ratios(financial_data: dict) -> dict:
    total_assets = financial_data.get('total_assets', 0)
    total_liabilities = financial_data.get('total_liabilities', 0)
    equity = total_assets - total_liabilities
    
    net_income = financial_data.get('net_income', 0)
    revenue = financial_data.get('revenue', 0)
    
    debt_to_equity = total_liabilities / equity if equity >= 0 else 0
    
    return_on_assets = (net_income / total_assets * 100) if total_assets > 0 else 0
    return_on_equity = (net_income / equity * 100) if equity > 0 else 0
    
    profit_margin = (net_income / revenue * 100) if revenue > 0 else 0
    
    asset_turnover = revenue / total_assets if total_assets > 0 else 0
    
    return {
        'debt_to_equity': debt_to_equity,
        'return_on_assets': return_on_assets,
        'return_on_equity': return_on_equity,
        'profit_margin': profit_margin,
        'asset_turnover': asset_turnover
    }

