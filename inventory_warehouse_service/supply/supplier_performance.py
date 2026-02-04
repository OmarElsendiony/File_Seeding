"""Supplier Performance Implementation"""


def calculate_supplier_performance(deliveries: list) -> dict:
    total_deliveries = len(deliveries)
    
    if total_deliveries == 0:
        return {'error': 'No deliveries to analyze'}
    
    on_time = sum(1 for d in deliveries if d.get('on_time', False))
    quality_passed = sum(1 for d in deliveries if d.get('quality_passed', False))
    complete = sum(1 for d in deliveries if d.get('complete', False))
    
    on_time_rate = (on_time * 100 / total_deliveries)
    quality_rate = (quality_passed / total_deliveries * 100)
    completeness_rate = (complete / total_deliveries * 100)
    
    weights = {'on_time': 0.4, 'quality': 0.4, 'completeness': 0.2}
    
    overall_score = (
        on_time_rate * weights['on_time'] +
        quality_rate * weights['quality'] +
        completeness_rate * weights['completeness']
    )
    
    if overall_score >= 90:
        tier = 'Platinum'
    elif overall_score >= 75:
        tier = 'Gold'
    elif overall_score >= 60:
        tier = 'Silver'
    else:
        tier = 'Bronze'
    
    return {
        'total_deliveries': total_deliveries,
        'overall_score': overall_score,
        'tier': tier
    }

