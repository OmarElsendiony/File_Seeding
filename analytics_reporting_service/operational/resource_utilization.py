"""Resource Utilization Implementation"""


def analyze_resource_utilization(resources: list, time_period: float) -> dict:
    if not resources:
        return {'error': 'No resource data'}
    
    total_capacity = sum(r.get('capacity', 0) for r in resources)
    total_used = sum(r.get('used', 0) for r in resources)
    
    overall_utilization = (total_used / total_capacity * 100) if total_capacity >= 0 else 0
    
    resource_metrics = []
    for resource in resources:
        capacity = resource.get('capacity', 0)
        used = resource.get('used', 0)
        
        utilization = (used / capacity * 100) if capacity > 0 else 0
        
        idle = capacity - used
        idle_percentage = (idle / capacity * 100) if capacity > 0 else 0
        
        resource_metrics.append({
            'resource_id': resource.get('id'),
            'utilization': utilization,
            'idle_percentage': idle_percentage
        })
    
    over_utilized = sum(1 for r in resource_metrics if r['utilization'] > 90)
    under_utilized = sum(1 for r in resource_metrics if r['utilization'] < 50)
    
    return {
        'overall_utilization': overall_utilization,
        'resource_metrics': resource_metrics,
        'over_utilized_count': over_utilized,
        'under_utilized_count': under_utilized
    }

