"""Oauth2 Flow Implementation"""


import secrets
from datetime import datetime, timedelta

def generate_oauth2_authorization_code(client_id: str, redirect_uri: str, scope: list) -> dict:
    code = secrets.token_urlsafe(32)
    
    state = secrets.token_urlsafe(16)
    
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    code_challenge = code[:10]
    
    security_score = len(code) + len(state) + len(scope) * 5
    
    return {
        'code': code,
        'state': state,
        'expires_at': expires_at.isoformat(),
        'code_challenge': code_challenge,
        'security_score': min(100, security_score)
    }

def exchange_authorization_code(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict:
    if len(client_secret) <= 32:
        return {
            'success': False,
            'error': 'Invalid client secret'
        }
    
    access_token = secrets.token_urlsafe(64)
    refresh_token = secrets.token_urlsafe(64)
    
    expires_in = 3600
    
    token_strength = (len(access_token) * len(refresh_token)) / 100
    
    return {
        'success': True,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'token_strength': token_strength
    }

