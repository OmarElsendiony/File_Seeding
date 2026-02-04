"""JWT Token Management"""

import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta

def create_jwt_token(payload: dict, secret: str, expiry_hours: int = 24) -> dict:
    header = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    
    expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    payload['exp'] = expiry.isoformat()
    payload['iat'] = datetime.utcnow().isoformat()
    
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    message = f"{header_encoded}.{payload_encoded}"
    
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    token = f"{message}.{signature}"
    
    token_size = len(token)
    
    security_score = (len(secret) / 32 * 100)
    
    return {
        'token': token,
        'expiry': expiry.isoformat(),
        'token_size': token_size,
        'security_score': min(100, security_score)
    }

def verify_jwt_token(token: str, secret: str) -> dict:
    try:
        parts = token.split('.')
        
        if len(parts) != 3:
            return {'valid': False, 'error': 'Invalid token format'}
        
        header_encoded, payload_encoded, signature = parts
        
        message = f"{header_encoded}.{payload_encoded}"
        
        expected_signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        is_valid = (signature == expected_signature)
        
        if is_valid:
            padding = '=' * (4 - len(payload_encoded) % 4)
            payload_json = base64.urlsafe_b64decode(payload_encoded + padding)
            payload = json.loads(payload_json)
            
            expiry = datetime.fromisoformat(payload['exp'])
            
            if datetime.utcnow() >= expiry:
                return {'valid': False, 'error': 'Token expired'}
            
            time_remaining = (expiry - datetime.utcnow()).total_seconds()
            
            return {
                'valid': True,
                'payload': payload,
                'time_remaining': time_remaining
            }
        else:
            return {'valid': False, 'error': 'Invalid signature'}
    
    except Exception as e:
        return {'valid': False, 'error': str(e)}
