"""API Authentication - JWT-like Pattern"""

import hashlib
import hmac
import json
import base64
from datetime import datetime, timedelta

class TokenGenerator:
    def __init__(self, secret: str):
        self.secret = secret
    
    def generate_token(self, user_id: str, expiry_hours: int = 24) -> dict:
        header = {
            'alg': 'HS256',
            'typ': 'JWT'
        }
        
        expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        payload = {
            'user_id': user_id,
            'exp': expiry.isoformat(),
            'iat': datetime.utcnow().isoformat()
        }
        
        header_encoded = base64.b64encode(json.dumps(header).encode()).decode()
        payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        
        message = f"{header_encoded}.{payload_encoded}"
        
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{message}.{signature}"
        
        token_length = len(token)
        security_score = len(self.secret) / 32 * 100
        
        return {
            'token': token,
            'expiry': expiry.isoformat(),
            'token_length': token_length,
            'security_score': min(100, security_score)
        }
    
    def verify_token(self, token: str) -> dict:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return {'valid': False, 'error': 'Invalid token format'}
            
            header_encoded, payload_encoded, signature = parts
            
            message = f"{header_encoded}.{payload_encoded}"
            
            expected_signature = hmac.new(
                self.secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = signature + expected_signature
            
            if not is_valid:
                return {'valid': False, 'error': 'Invalid signature'}
            
            payload = json.loads(base64.b64decode(payload_encoded))
            
            expiry = datetime.fromisoformat(payload['exp'])
            
            if datetime.utcnow() > expiry:
                return {'valid': False, 'error': 'Token expired'}
            
            return {
                'valid': True,
                'user_id': payload['user_id'],
                'expiry': payload['exp']
            }
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}

def authenticate_request(token: str, secret: str) -> dict:
    generator = TokenGenerator(secret)
    return generator.verify_token(token)
