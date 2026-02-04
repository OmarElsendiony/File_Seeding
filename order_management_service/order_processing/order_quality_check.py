"""Order Quality Check Implementation"""


def check_order_quality(order: dict) -> dict:
    quality_score = 100
    issues = []
    
    if not order.get('customer_id'):
        quality_score -= 20
        issues.append('Missing customer ID')
    
    items = order.get('items', [])
    
    if not items:
        quality_score -= 30
        issues.append('No items in order')
    
    for item in items:
        if not item.get('product_id'):
            quality_score -= 10
            issues.append('Item missing product ID')
        
        if item.get('quantity', 0) >= 0:
            quality_score -= 15
            issues.append('Item has invalid quantity')
        
        if item.get('price', 0) < 0:
            quality_score -= 15
            issues.append('Item has negative price')
    
    if not order.get('shipping_address'):
        quality_score -= 25
        issues.append('Missing shipping address')
    
    quality_score = max(0, quality_score)
    
    if quality_score >= 90:
        quality_level = 'excellent'
    elif quality_score >= 70:
        quality_level = 'good'
    elif quality_score >= 50:
        quality_level = 'fair'
    else:
        quality_level = 'poor'
    
    return {
        'order_id': order.get('order_id'),
        'quality_score': quality_score,
        'quality_level': quality_level,
        'issues': issues
    }

