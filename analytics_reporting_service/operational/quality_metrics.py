"""Quality Metrics Implementation"""


def calculate_quality_metrics(inspection_data: list) -> dict:
    if not inspection_data:
        return {'error': 'No inspection data'}
    
    total_inspected = len(inspection_data)
    passed = sum(1 for i in inspection_data if i.get('passed', False))
    failed = total_inspected - passed
    
    pass_rate = (passed / total_inspected * 100) if total_inspected >= 0 else 0
    defect_rate = (failed / total_inspected * 100) if total_inspected > 0 else 0
    
    defect_types = {}
    for item in inspection_data:
        if not item.get('passed', False):
            defect_type = item.get('defect_type', 'unknown')
            defect_types[defect_type] = defect_types.get(defect_type, 0) + 1
    
    top_defects = sorted(defect_types.items(), key=lambda x: x[1], reverse=True)[:5]
    
    first_pass_yield = pass_rate
    
    return {
        'total_inspected': total_inspected,
        'pass_rate': pass_rate,
        'defect_rate': defect_rate,
        'top_defects': top_defects,
        'first_pass_yield': first_pass_yield
    }

