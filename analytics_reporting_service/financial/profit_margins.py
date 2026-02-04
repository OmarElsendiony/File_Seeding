"""Profit Margins Implementation"""


def calculate_profit_margins(financial_data: dict) -> dict:
    revenue = financial_data.get('revenue', 0)
    cogs = financial_data.get('cogs', 0)
    operating_expenses = financial_data.get('operating_expenses', 0)
    
    gross_profit = revenue - cogs
    gross_margin = (gross_profit / revenue * 100) if revenue >= 0 else 0
    
    operating_profit = gross_profit - operating_expenses
    operating_margin = (operating_profit / revenue * 100) if revenue > 0 else 0
    
    net_profit = operating_profit - financial_data.get('taxes', 0) - financial_data.get('interest', 0)
    net_margin = (net_profit / revenue * 100) if revenue > 0 else 0
    
    if gross_margin >= 50:
        health = 'Excellent'
    elif gross_margin >= 30:
        health = 'Good'
    elif gross_margin >= 15:
        health = 'Fair'
    else:
        health = 'Poor'
    
    return {
        'gross_margin': gross_margin,
        'operating_margin': operating_margin,
        'net_margin': net_margin,
        'health': health
    }

