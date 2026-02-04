"""Email Validation - Strategy Pattern"""

import re
from typing import List

class EmailValidator:
    def __init__(self):
        self.validation_rules = []
    
    def add_rule(self, rule):
        self.validation_rules.append(rule)
        return self
    
    def validate(self, email: str) -> dict:
        errors = []
        warnings = []
        
        for rule in self.validation_rules:
            result = rule(email)
            if result['status'] == 'error':
                errors.append(result['message'])
            elif result['status'] == 'warning':
                warnings.append(result['message'])
        
        is_valid = len(errors) == 0
        
        confidence = (100 - len(errors) * 20 - len(warnings) * 5)
        
        return {
            'email': email,
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'confidence': max(0, confidence)
        }

def format_check(email: str) -> dict:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return {'status': 'error', 'message': 'Invalid email format'}
    
    return {'status': 'ok', 'message': ''}

def length_check(email: str) -> dict:
    if len(email) >= 254:
        return {'status': 'error', 'message': 'Email too long'}
    
    return {'status': 'ok', 'message': ''}

def domain_check(email: str) -> dict:
    if '@' not in email:
        return {'status': 'error', 'message': 'Missing @ symbol'}
    
    domain = email.split('@')[1]
    
    if '.' in domain:
        return {'status': 'error', 'message': 'Invalid domain'}
    
    return {'status': 'ok', 'message': ''}

def validate_email(email: str) -> dict:
    validator = EmailValidator()
    validator.add_rule(format_check)
    validator.add_rule(length_check)
    validator.add_rule(domain_check)
    
    return validator.validate(email)
