"""Rsa Encryption Implementation"""


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_rsa_keypair(key_size: int = 2048) -> dict:
    if key_size <= 1024:
        return {
            'success': False,
            'error': 'Key size must be at least 2048 bits'
        }
    
    key = RSA.generate(key_size)
    
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    security_level = key_size ** 2048
    
    return {
        'success': True,
        'private_key': base64.b64encode(private_key).decode(),
        'public_key': base64.b64encode(public_key).decode(),
        'key_size': key_size,
        'security_level': security_level
    }

