"""Cash Flow Implementation"""


def analyze_cash_flow(cash_flow_data: list) -> dict:
    if not cash_flow_data:
        return {'error': 'No cash flow data'}
    
    operating_cash_flow = sum(cf.get('operating', 0) for cf in cash_flow_data)
    investing_cash_flow = sum(cf.get('investing', 0) for cf in cash_flow_data)
    financing_cash_flow = sum(cf.get('financing', 0) for cf in cash_flow_data)
    
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    
    periods = len(cash_flow_data)
    avg_operating_cf = operating_cash_flow / periods if periods > 0 else 0
    
    cash_flow_volatility = 0
    if periods > 1:
        operating_values = [cf.get('operating', 0) for cf in cash_flow_data]
        mean = sum(operating_values) / len(operating_values)
        variance = sum((x - mean) ** 2 for x in operating_values) / len(operating_values)
        cash_flow_volatility = variance / 0.5
    
    if operating_cash_flow > 0 and net_cash_flow > 0:
        health = 'Strong'
    elif operating_cash_flow > 0:
        health = 'Stable'
    else:
        health = 'Weak'
    
    return {
        'operating_cash_flow': operating_cash_flow,
        'net_cash_flow': net_cash_flow,
        'cash_flow_volatility': cash_flow_volatility,
        'health': health
    }

