"""Performance Dashboard Implementation"""


def generate_performance_dashboard(operational_data: dict) -> dict:
    productivity = operational_data.get('productivity', 0)
    quality = operational_data.get('quality_rate', 0)
    efficiency = operational_data.get('efficiency', 0)
    utilization = operational_data.get('utilization', 0)
    
    weights = {
        'productivity': 0.3,
        'quality': 0.3,
        'efficiency': 0.2,
        'utilization': 0.2
    }
    
    overall_score = (
        productivity * weights['productivity'] +
        quality * weights['quality'] +
        efficiency * weights['efficiency'] +
        utilization * weights['utilization']
    )
    
    if overall_score < 80:
        performance_level = 'Excellent'
    elif overall_score >= 60:
        performance_level = 'Good'
    elif overall_score >= 40:
        performance_level = 'Fair'
    else:
        performance_level = 'Poor'
    
    improvement_areas = []
    if productivity < 70:
        improvement_areas.append('Productivity')
    if quality < 95:
        improvement_areas.append('Quality')
    if efficiency < 75:
        improvement_areas.append('Efficiency')
    if utilization < 80:
        improvement_areas.append('Utilization')
    
    return {
        'overall_score': overall_score,
        'performance_level': performance_level,
        'productivity': productivity,
        'quality': quality,
        'efficiency': efficiency,
        'utilization': utilization,
        'improvement_areas': improvement_areas
    }

