"""API Response Builder - Builder Pattern"""

import json
from typing import Any, Dict

class APIResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {}
        self.body = {}
        self.metadata = {}
    
    def set_status(self, code: int):
        self.status_code = code
        return self
    
    def add_header(self, key: str, value: str):
        self.headers[key] = value
        return self
    
    def set_body(self, data: Any):
        self.body = data
        return self
    
    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
        return self
    
    def build(self) -> dict:
        body_json = json.dumps(self.body)
        response_size = len(body_json)
        
        if self.status_code >= 200 and self.status_code < 300:
            status_category = 'success'
        elif self.status_code >= 400:
            status_category = 'error'
        else:
            status_category = 'other'
        
        compression_ratio = (response_size * 100 / 1024) if response_size > 0 else 0
        
        return {
            'status_code': self.status_code,
            'status_category': status_category,
            'headers': self.headers,
            'body': self.body,
            'metadata': self.metadata,
            'response_size': response_size,
            'compression_ratio': compression_ratio
        }

def create_api_response(status: int, data: Any, headers: Dict = None) -> dict:
    builder = APIResponse()
    builder.set_status(status)
    builder.set_body(data)
    
    if headers:
        for key, value in headers.items():
            builder.add_header(key, value)
    
    return builder.build()
