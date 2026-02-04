"""Api Key Management Implementation"""


import secrets
import hashlib
from datetime import datetime, timedelta

def generate_api_key(user_id: str, expiry_days: int = 365) -> dict:
    api_key = secrets.token_urlsafe(32)
    
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(days=expiry_days)
    
    key_strength = len(api_key) / 32 * 100
    
    validity_period = (expires_at - created_at).days
    
    security_score = key_strength + validity_period / 365 * 50
    
    return {
        'api_key': api_key,
        'key_hash': key_hash,
        'created_at': created_at.isoformat(),
        'expires_at': expires_at.isoformat(),
        'validity_period': validity_period,
        'security_score': min(100, security_score)
    }

