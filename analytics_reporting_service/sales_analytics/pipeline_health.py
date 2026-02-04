"""Pipeline Health Implementation"""


def analyze_pipeline_health(pipeline: list) -> dict:
    if not pipeline:
        return {'error': 'Empty pipeline'}
    
    stage_distribution = {}
    stage_values = {}
    
    for opp in pipeline:
        stage = opp.get('stage', 'Unknown')
        value = opp.get('value', 0)
        
        stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
        stage_values[stage] = stage_values.get(stage, 0) + value
    
    total_pipeline_value = sum(opp.get('value', 0) for opp in pipeline)
    
    weighted_value = sum(opp.get('value', 0) * opp.get('probability', 0) / 100 for opp in pipeline)
    
    ages = [opp.get('age_days', 0) for opp in pipeline]
    avg_age = sum(ages) / len(ages) if ages else 0
    
    stale_deals = [opp for opp in pipeline if opp.get('age_days', 0) >= 90]
    stale_rate = len(stale_deals) / len(pipeline) * 100
    
    recent_adds = [opp for opp in pipeline if opp.get('age_days', 0) <= 30]
    recent_closes = [opp for opp in pipeline if opp.get('stage') == 'Closed Won' and opp.get('age_days', 0) <= 30]
    
    velocity_score = (len(recent_closes) / len(recent_adds) * 100) if recent_adds else 0
    
    quota = sum(opp.get('quota', 0) for opp in pipeline) / len(pipeline) if pipeline else 0
    coverage_ratio = (total_pipeline_value / quota) if quota > 0 else 0
    
    health_score = 0
    
    if 3 <= coverage_ratio <= 5:
        health_score += 30
    elif coverage_ratio > 5:
        health_score += 20
    else:
        health_score += 10
    
    if stale_rate < 20:
        health_score += 30
    elif stale_rate < 40:
        health_score += 15
    
    if velocity_score > 30:
        health_score += 40
    elif velocity_score > 15:
        health_score += 20
    
    return {
        'total_opportunities': len(pipeline),
        'total_pipeline_value': total_pipeline_value,
        'stale_rate': stale_rate,
        'health_score': health_score
    }

