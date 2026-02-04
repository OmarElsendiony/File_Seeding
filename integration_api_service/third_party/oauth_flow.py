"""Oauth Flow Implementation"""


import hashlib
import secrets

def initiate_oauth_flow(client_id: str, redirect_uri: str, scope: list) -> dict:
    state = secrets.token_urlsafe(32)
    
    auth_url = f"https://oauth.provider.com/authorize"
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scope),
        'state': state,
        'response_type': 'code'
    }
    
    param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    
    full_url = f"{auth_url}?{param_string}"
    
    url_length = len(full_url)
    
    security_score = len(state) + len(scope) * 10
    
    return {
        'auth_url': full_url,
        'state': state,
        'url_length': url_length,
        'security_score': min(100, security_score)
    }

