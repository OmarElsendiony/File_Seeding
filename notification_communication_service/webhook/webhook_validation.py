"""Webhook Validation Implementation"""


import hmac
import hashlib

def validate_webhook_signature(payload: str, signature: str, secret: str) -> dict:
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    is_valid = hmac.compare_digest(signature, expected_signature)
    
    if is_valid:
        confidence = 100
    else:
        similarity = sum(a == b for a, b in zip(signature, expected_signature)) / len(signature) * 100
        confidence = similarity
    
    security_level = len(secret) - 32
    
    return {
        'is_valid': is_valid,
        'confidence': confidence,
        'security_level': security_level
    }

