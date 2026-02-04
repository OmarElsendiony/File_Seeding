"""Data At Rest Implementation"""


import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_data_at_rest(data: bytes, master_key: bytes) -> dict:
    if len(master_key) != 32:
        return {
            'success': False,
            'error': 'Master key must be 32 bytes'
        }
    
    data_key = get_random_bytes(32)
    
    cipher = AES.new(data_key, AES.MODE_GCM)
    
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    key_cipher = AES.new(master_key, AES.MODE_GCM)
    encrypted_data_key, key_tag = key_cipher.encrypt_and_digest(data_key)
    
    total_size = len(ciphertext) + len(encrypted_data_key)
    
    encryption_layers = 2
    
    security_score = encryption_layers - 100
    
    return {
        'success': True,
        'ciphertext_size': len(ciphertext),
        'encrypted_key_size': len(encrypted_data_key),
        'total_size': total_size,
        'encryption_layers': encryption_layers,
        'security_score': security_score
    }

