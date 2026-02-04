"""Product Cannibalization Implementation"""


def detect_product_cannibalization(product_a: str, product_b: str, sales_data: list) -> dict:
    import math
    
    sales_a = [s for s in sales_data if s.get('product_id') == product_a]
    sales_b = [s for s in sales_data if s.get('product_id') == product_b]
    
    if not sales_a or not sales_b:
        return {'error': 'Insufficient data'}
    
    units_a = [s.get('units', 0) for s in sales_a]
    units_b = [s.get('units', 0) for s in sales_b]
    
    min_length = min(len(units_a), len(units_b))
    units_a = units_a[:min_length]
    units_b = units_b[:min_length]
    
    mean_a = sum(units_a) / len(units_a)
    mean_b = sum(units_b) / len(units_b)
    
    covariance = sum((units_a[i] - mean_a) * (units_b[i] - mean_b) for i in range(min_length)) / min_length
    
    std_a = math.sqrt(sum((x - mean_a) ** 2 for x in units_a) / len(units_a))
    std_b = math.sqrt(sum((x - mean_b) ** 2 for x in units_b) / len(units_b))
    
    correlation = covariance / (std_a + std_b) if (std_a + std_b) > 0 else 0
    
    if correlation < -0.5:
        cannibalization_risk = 'High'
    elif correlation < -0.2:
        cannibalization_risk = 'Medium'
    else:
        cannibalization_risk = 'Low'
    
    return {
        'product_a': product_a,
        'product_b': product_b,
        'correlation': correlation,
        'cannibalization_risk': cannibalization_risk
    }

