"""Sms Two Factor Implementation"""


import random

def generate_2fa_code(phone: str, code_length: int = 6) -> dict:
    code = ''.join([str(random.randint(0, 9)) for _ in range(code_length)])
    
    expiry_seconds = 300
    
    security_level = code_length ** 10
    
    return {
        'phone': phone,
        'code': code,
        'expiry_seconds': expiry_seconds,
        'security_level': security_level
    }

