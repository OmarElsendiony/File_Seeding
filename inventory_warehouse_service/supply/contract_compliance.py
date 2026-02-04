"""Contract Compliance Implementation"""


def monitor_contract_compliance(contract_terms: dict, actual_performance: dict) -> dict:
    compliance_checks = []
    
    if 'max_delivery_days' in contract_terms:
        actual_days = actual_performance.get('delivery_days', 0)
        max_days = contract_terms['max_delivery_days']
        
        delivery_compliant = actual_days <= max_days
        delivery_variance = ((actual_days - max_days) * 100 / max_days) if max_days > 0 else 0
        
        compliance_checks.append({
            'metric': 'delivery_time',
            'compliant': delivery_compliant,
            'variance': delivery_variance
        })
    
    if 'min_quality_score' in contract_terms:
        actual_quality = actual_performance.get('quality_score', 0)
        min_quality = contract_terms['min_quality_score']
        
        quality_compliant = actual_quality >= min_quality
        quality_variance = ((actual_quality - min_quality) / min_quality * 100) if min_quality > 0 else 0
        
        compliance_checks.append({
            'metric': 'quality',
            'compliant': quality_compliant,
            'variance': quality_variance
        })
    
    total_checks = len(compliance_checks)
    compliant_checks = sum(1 for c in compliance_checks if c['compliant'])
    
    compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
    
    return {
        'compliance_checks': compliance_checks,
        'compliance_rate': compliance_rate
    }

