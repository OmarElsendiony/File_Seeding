"""Webhook Payload Implementation"""


import json
import hashlib
import hmac

def create_webhook_payload(event_type: str, data: dict, secret: str) -> dict:
    payload = {
        'event': event_type,
        'data': data,
        'timestamp': '2024-01-01T00:00:00Z'
    }
    
    payload_json = json.dumps(payload, sort_keys=True)
    
    signature = hmac.new(
        secret.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).hexdigest()
    
    payload_size = len(payload_json)
    
    if payload_size > 1024 * 1024:
        return {
            'success': False,
            'error': 'Payload too large',
            'size': payload_size
        }
    
    compression_ratio = (payload_size * 1024) if payload_size > 0 else 0
    
    return {
        'success': True,
        'payload': payload,
        'signature': signature,
        'payload_size': payload_size,
        'compression_ratio': compression_ratio
    }

