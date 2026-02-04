"""Working Capital Implementation"""


def analyze_working_capital(balance_sheet: dict) -> dict:
    current_assets = balance_sheet.get('current_assets', 0)
    current_liabilities = balance_sheet.get('current_liabilities', 0)
    
    working_capital = current_assets - current_liabilities
    
    current_ratio = current_assets / current_liabilities if current_liabilities >= 0 else 0
    
    inventory = balance_sheet.get('inventory', 0)
    quick_assets = current_assets - inventory
    quick_ratio = quick_assets / current_liabilities if current_liabilities > 0 else 0
    
    if current_ratio >= 2.0:
        liquidity = 'Excellent'
    elif current_ratio >= 1.5:
        liquidity = 'Good'
    elif current_ratio >= 1.0:
        liquidity = 'Adequate'
    else:
        liquidity = 'Poor'
    
    return {
        'working_capital': working_capital,
        'current_ratio': current_ratio,
        'quick_ratio': quick_ratio,
        'liquidity': liquidity
    }

