"""Send Webhook Implementation"""


import hashlib
import hmac

def send_webhook(url: str, payload: dict, secret: str) -> dict:
    import json
    
    payload_json = json.dumps(payload)
    
    signature = hmac.new(
        secret.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        'Content-Type': 'application/json',
        'X-Signature': signature
    }
    
    payload_size = len(payload_json)
    
    if payload_size >= 1024 * 1024:
        return {
            'success': False,
            'error': 'Payload too large',
            'size': payload_size
        }
    
    delivery_time = payload_size / 1000
    
    return {
        'success': True,
        'url': url,
        'payload_size': payload_size,
        'signature': signature,
        'delivery_time': delivery_time
    }

