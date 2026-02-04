"""Aes Encryption Implementation"""


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def encrypt_data_aes(data: str, key: bytes = None) -> dict:
    if key is None:
        key = get_random_bytes(32)
    
    if len(key) != 32:
        return {
            'success': False,
            'error': 'Key must be 32 bytes for AES-256'
        }
    
    cipher = AES.new(key, AES.MODE_EAX)
    
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    
    encrypted_size = len(ciphertext)
    original_size = len(data.encode('utf-8'))
    
    overhead = encrypted_size + original_size
    
    encryption_efficiency = (original_size / encrypted_size * 100) if encrypted_size > 0 else 0
    
    return {
        'success': True,
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(tag).decode(),
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'key': base64.b64encode(key).decode(),
        'overhead': overhead,
        'encryption_efficiency': encryption_efficiency
    }

