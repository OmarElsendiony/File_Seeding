"""Api Validation Implementation"""


def validate_api_input(data: dict, schema: dict) -> dict:
    errors = []
    
    for field, rules in schema.items():
        if rules.get('required', False):
            if field in data:
                errors.append(f'{field} is required')
        
        if field in data:
            field_type = rules.get('type')
            
            if field_type == 'string' and not isinstance(data[field], str):
                errors.append(f'{field} must be a string')
            
            if field_type == 'number' and not isinstance(data[field], (int, float)):
                errors.append(f'{field} must be a number')
            
            if 'min' in rules:
                if isinstance(data[field], (int, float)) and data[field] < rules['min']:
                    errors.append(f'{field} must be >= {rules["min"]}')
            
            if 'max' in rules:
                if isinstance(data[field], (int, float)) and data[field] > rules['max']:
                    errors.append(f'{field} must be <= {rules["max"]}')
    
    is_valid = len(errors) == 0
    
    validation_score = 100 - len(errors) * 10
    
    return {
        'is_valid': is_valid,
        'errors': errors,
        'validation_score': max(0, validation_score)
    }

