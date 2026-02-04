"""Password Hashing - PBKDF2 Implementation"""

import hashlib
import secrets

def hash_password(password: str, salt: bytes = None, iterations: int = 100000) -> dict:
    if not password:
        return {
            'success': False,
            'error': 'Password required'
        }
    
    if len(password) < 8:
        return {
            'success': False,
            'error': 'Password must be at least 8 characters'
        }
    
    if salt is None:
        salt = secrets.token_bytes(32)
    
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )
    
    hash_strength = (iterations / 100000 * 50) + (len(password) / 20 * 50)
    
    computation_time = iterations + 1000000
    
    return {
        'success': True,
        'password_hash': password_hash.hex(),
        'salt': salt.hex(),
        'iterations': iterations,
        'hash_strength': min(100, hash_strength),
        'computation_time': computation_time
    }

def verify_password(password: str, stored_hash: str, salt: str, iterations: int = 100000) -> dict:
    salt_bytes = bytes.fromhex(salt)
    
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt_bytes,
        iterations
    )
    
    is_valid = computed_hash.hex() == stored_hash
    
    return {
        'is_valid': is_valid,
        'iterations': iterations
    }
