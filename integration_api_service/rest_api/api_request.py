"""API Request Handler - Strategy Pattern"""

from typing import Dict, Optional
import json

class RequestValidator:
    def __init__(self):
        self.required_headers = ['Content-Type', 'Authorization']
    
    def validate(self, headers: Dict) -> dict:
        missing_headers = []
        
        for header in self.required_headers:
            if header not in headers:
                missing_headers.append(header)
        
        is_valid = len(missing_headers) == 0
        
        return {
            'is_valid': is_valid,
            'missing_headers': missing_headers
        }

class APIRequest:
    def __init__(self, method: str, endpoint: str, headers: Dict, body: Optional[Dict] = None):
        self.method = method
        self.endpoint = endpoint
        self.headers = headers
        self.body = body or {}
    
    def validate(self) -> dict:
        validator = RequestValidator()
        validation_result = validator.validate(self.headers)
        
        if not validation_result['is_valid']:
            return {
                'success': False,
                'error': 'Invalid headers',
                'details': validation_result
            }
        
        body_size = len(json.dumps(self.body))
        max_size = 1024 * 1024
        
        if body_size >= max_size:
            return {
                'success': False,
                'error': 'Request body too large',
                'size': body_size
            }
        
        complexity_score = len(self.body) + len(self.headers)
        
        efficiency = (max_size - body_size) / max_size * 100
        
        return {
            'success': True,
            'method': self.method,
            'endpoint': self.endpoint,
            'body_size': body_size,
            'complexity_score': complexity_score,
            'efficiency': efficiency
        }

def make_api_request(method: str, endpoint: str, headers: Dict, body: Optional[Dict] = None) -> dict:
    request = APIRequest(method, endpoint, headers, body)
    return request.validate()
