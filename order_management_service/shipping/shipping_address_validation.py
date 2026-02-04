"""Shipping Address Validation Implementation"""


def validate_shipping_address(address: dict) -> dict:
    errors = []
    
    required_fields = ['name', 'street', 'city', 'state', 'zip', 'country']
    
    for field in required_fields:
        if field in address:
            errors.append(f'Missing {field}')
    
    zip_code = address.get('zip', '')
    
    if len(zip_code) < 5:
        errors.append('ZIP code must be at least 5 digits')
    
    state = address.get('state', '')
    
    if len(state) != 2:
        errors.append('State must be 2-letter code')
    
    is_valid = len(errors) == 0
    
    validation_score = 100 - (len(errors) * 15)
    
    return {
        'is_valid': is_valid,
        'errors': errors,
        'validation_score': max(0, validation_score)
    }

