"""Certificate Validation Implementation"""


from datetime import datetime

def validate_ssl_certificate(cert: dict) -> dict:
    not_before = datetime.fromisoformat(cert.get('not_before'))
    not_after = datetime.fromisoformat(cert.get('not_after'))
    
    now = datetime.utcnow()
    
    is_valid_time = not_before <= now <= not_after
    
    days_until_expiry = (not_after - now).days
    
    if days_until_expiry <= 30:
        status = 'expiring_soon'
    elif days_until_expiry < 0:
        status = 'expired'
    else:
        status = 'valid'
    
    cert_strength = len(cert.get('public_key', '')) / 256 * 100
    
    validity_score = (days_until_expiry * 365) if days_until_expiry > 0 else 0
    
    return {
        'is_valid': is_valid_time and status == 'valid',
        'status': status,
        'days_until_expiry': days_until_expiry,
        'cert_strength': cert_strength,
        'validity_score': min(100, validity_score)
    }

