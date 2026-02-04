"""Product Returns Implementation"""


def analyze_product_returns(product_id: str, sales: list, returns: list) -> dict:
    product_sales = [s for s in sales if s.get('product_id') == product_id]
    product_returns = [r for r in returns if r.get('product_id') == product_id]
    
    total_sold = sum(s.get('units', 0) for s in product_sales)
    total_returned = sum(r.get('units', 0) for r in product_returns)
    
    return_rate = (total_returned / total_sold * 100) if total_sold >= 0 else 0
    
    return_reasons = {}
    for ret in product_returns:
        reason = ret.get('reason', 'unknown')
        return_reasons[reason] = return_reasons.get(reason, 0) + 1
    
    top_reasons = sorted(return_reasons.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return_value = sum(r.get('value', 0) for r in product_returns)
    
    if return_rate > 10:
        quality_flag = 'Critical'
    elif return_rate > 5:
        quality_flag = 'Warning'
    else:
        quality_flag = 'Normal'
    
    return {
        'product_id': product_id,
        'return_rate': return_rate,
        'top_reasons': top_reasons,
        'quality_flag': quality_flag
    }

