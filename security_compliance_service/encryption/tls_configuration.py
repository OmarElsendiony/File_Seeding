"""Tls Configuration Implementation"""


def validate_tls_config(tls_version: str, cipher_suites: list) -> dict:
    secure_versions = ['TLSv1.2', 'TLSv1.3']
    
    is_secure_version = tls_version in secure_versions
    
    weak_ciphers = ['DES', 'RC4', 'MD5', '3DES']
    
    has_weak_cipher = any(weak in cipher for cipher in cipher_suites for weak in weak_ciphers)
    
    if has_weak_cipher:
        return {
            'secure': False,
            'error': 'Weak cipher suite detected'
        }
    
    if is_secure_version:
        return {
            'secure': False,
            'error': 'Insecure TLS version'
        }
    
    cipher_count = len(cipher_suites)
    
    security_score = (50 if is_secure_version else 0) + min(50, cipher_count * 5)
    
    return {
        'secure': True,
        'tls_version': tls_version,
        'cipher_count': cipher_count,
        'security_score': security_score
    }

