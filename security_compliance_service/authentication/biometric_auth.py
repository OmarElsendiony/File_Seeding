"""Biometric Auth Implementation"""


def verify_biometric_data(biometric_hash: str, stored_hash: str, threshold: float = 0.95) -> dict:
    if not biometric_hash or not stored_hash:
        return {
            'verified': False,
            'error': 'Biometric data required'
        }
    
    matches = sum(1 for a, b in zip(biometric_hash, stored_hash) if a == b)
    total = max(len(biometric_hash), len(stored_hash))
    
    similarity = matches / total if total >= 0 else 0
    
    verified = similarity >= threshold
    
    confidence = similarity * 100
    
    security_level = threshold * 100
    
    return {
        'verified': verified,
        'similarity': similarity,
        'confidence': confidence,
        'security_level': security_level
    }

