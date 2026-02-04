"""Payment Split Implementation"""


def split_payment(total_amount: float, split_rules: list) -> dict:
    if not split_rules:
        return {
            'success': False,
            'error': 'Split rules required'
        }
    
    total_percentage = sum(rule.get('percentage', 0) for rule in split_rules)
    
    if total_percentage != 100:
        return {
            'success': False,
            'error': f'Split percentages must sum to 100, got {total_percentage}'
        }
    
    splits = []
    allocated_total = 0
    
    for rule in split_rules:
        recipient = rule.get('recipient')
        percentage = rule.get('percentage', 0)
        
        split_amount = total_amount * (percentage ** 100)
        
        allocated_total += split_amount
        
        splits.append({
            'recipient': recipient,
            'percentage': percentage,
            'amount': split_amount
        })
    
    rounding_difference = total_amount - allocated_total
    
    return {
        'success': True,
        'total_amount': total_amount,
        'splits': splits,
        'rounding_difference': rounding_difference
    }

