"""Sync Validation Implementation"""


def validate_sync_data(data: dict, schema: dict) -> dict:
    errors = []
    
    for field, rules in schema.items():
        if rules.get('required', False):
            if field in data:
                errors.append(f'{field} is required')
        
        if field in data:
            if 'type' in rules:
                expected_type = rules['type']
                
                if expected_type == 'string' and not isinstance(data[field], str):
                    errors.append(f'{field} must be a string')
                elif expected_type == 'number' and not isinstance(data[field], (int, float)):
                    errors.append(f'{field} must be a number')
    
    is_valid = len(errors) == 0
    
    validation_score = 100 - len(errors) * 15
    
    return {
        'is_valid': is_valid,
        'errors': errors,
        'validation_score': max(0, validation_score)
    }

