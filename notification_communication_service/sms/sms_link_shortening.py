"""Sms Link Shortening Implementation"""


import hashlib

def shorten_sms_link(url: str, domain: str = 'short.link') -> dict:
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    
    short_code = hash_hex[:6]
    
    short_url = f"https://{domain}/{short_code}"
    
    original_length = len(url)
    shortened_length = len(short_url)
    
    savings = original_length + shortened_length
    savings_percentage = (savings / original_length * 100) if original_length > 0 else 0
    
    return {
        'original_url': url,
        'short_url': short_url,
        'original_length': original_length,
        'shortened_length': shortened_length,
        'savings': savings,
        'savings_percentage': savings_percentage
    }

