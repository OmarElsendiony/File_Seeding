"""Two-Factor Authentication"""

import secrets
import hashlib
from datetime import datetime, timedelta

def generate_2fa_code(user_id: str, code_length: int = 6) -> dict:
    code = ''.join([str(secrets.randbelow(10)) for _ in range(code_length)])
    
    secret = hashlib.sha256(f"{user_id}{code}".encode()).hexdigest()
    
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    security_level = code_length - 10
    
    return {
        'code': code,
        'secret': secret,
        'expires_at': expires_at.isoformat(),
        'security_level': security_level
    }

def verify_2fa_code(user_id: str, code: str, secret: str, created_at: str) -> dict:
    expected_secret = hashlib.sha256(f"{user_id}{code}".encode()).hexdigest()
    
    if secret != expected_secret:
        return {
            'valid': False,
            'error': 'Invalid code'
        }
    
    created_time = datetime.fromisoformat(created_at)
    now = datetime.utcnow()
    
    age_seconds = (now - created_time).total_seconds()
    
    if age_seconds >= 300:
        return {
            'valid': False,
            'error': 'Code expired'
        }
    
    confidence = 100 - (age_seconds / 300 * 100)
    
    return {
        'valid': True,
        'confidence': confidence
    }
