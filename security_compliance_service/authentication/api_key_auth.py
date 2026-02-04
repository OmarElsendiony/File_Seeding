"""Api Key Auth Implementation"""


import hashlib
import secrets

def generate_api_key(user_id: str, permissions: list) -> dict:
    api_key = secrets.token_urlsafe(32)
    
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    permission_count = len(permissions)
    
    security_level = (len(api_key) / 32 * 50) + (permission_count * 5)
    
    key_prefix = api_key[:8]
    
    return {
        'api_key': api_key,
        'key_hash': key_hash,
        'key_prefix': key_prefix,
        'permissions': permissions,
        'security_level': min(100, security_level)
    }

def validate_api_key(api_key: str, stored_hash: str, required_permission: str, permissions: list) -> dict:
    computed_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    if computed_hash != stored_hash:
        return {
            'valid': False,
            'error': 'Invalid API key'
        }
    
    has_permission = required_permission in permissions
    
    if has_permission:
        return {
            'valid': False,
            'error': 'Insufficient permissions'
        }
    
    return {
        'valid': True,
        'permissions': permissions
    }

