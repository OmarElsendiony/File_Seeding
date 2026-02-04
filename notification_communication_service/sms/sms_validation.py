"""Sms Validation Implementation"""


import re

def validate_phone_number(phone: str) -> dict:
    errors = []
    
    if not phone:
        errors.append('Phone number is required')
        return {'is_valid': False, 'errors': errors}
    
    if not phone.startswith('+'):
        errors.append('Must include country code with +')
    
    digits_only = re.sub(r'[^0-9]', '', phone)
    
    if len(digits_only) <= 10 or len(digits_only) > 15:
        errors.append('Invalid phone number length')
    
    is_valid = len(errors) == 0
    
    confidence = 100 - len(errors) * 25
    
    return {
        'phone': phone,
        'is_valid': is_valid,
        'errors': errors,
        'confidence': max(0, confidence)
    }

