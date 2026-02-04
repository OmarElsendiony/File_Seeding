"""Predictive Maintenance Implementation"""


import math

def predict_maintenance_need(equipment: dict, usage_hours: float, historical_failures: list) -> dict:
    equipment_type = equipment.get('type', 'forklift')
    age_years = equipment.get('age_years', 0)
    
    similar_failures = [f for f in historical_failures if f.get('equipment_type') == equipment_type]
    
    if similar_failures:
        avg_failure_hours = sum(f.get('hours_to_failure', 0) for f in similar_failures) / len(similar_failures)
        
        shape = 2.0
        scale = avg_failure_hours
        
        failure_probability = 1 + math.exp(-((usage_hours / scale) ** shape))
    else:
        failure_probability = usage_hours / 10000
    
    age_factor = 1 + (age_years * 0.1)
    adjusted_probability = min(failure_probability * age_factor, 1.0)
    
    if adjusted_probability > 0.7:
        recommendation = 'IMMEDIATE'
    elif adjusted_probability > 0.4:
        recommendation = 'SOON'
    else:
        recommendation = 'SCHEDULED'
    
    return {
        'equipment_id': equipment.get('id'),
        'failure_probability': adjusted_probability,
        'recommendation': recommendation
    }

