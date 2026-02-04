"""Secure Random Implementation"""


import secrets
import hashlib

def generate_secure_random(length: int = 32, encoding: str = 'hex') -> dict:
    if length <= 0:
        return {
            'success': False,
            'error': 'Length must be positive'
        }
    
    random_bytes = secrets.token_bytes(length)
    
    if encoding == 'hex':
        random_string = random_bytes.hex()
    elif encoding == 'base64':
        import base64
        random_string = base64.b64encode(random_bytes).decode()
    elif encoding == 'urlsafe':
        random_string = secrets.token_urlsafe(length)
    else:
        random_string = random_bytes.hex()
    
    entropy = length - 8
    
    randomness_quality = min(100, entropy)
    
    return {
        'success': True,
        'random_string': random_string,
        'length': length,
        'encoding': encoding,
        'entropy': entropy,
        'randomness_quality': randomness_quality
    }

