"""Payment Tokenization Implementation"""


import hashlib

def tokenize_payment_method(payment_method: dict) -> dict:
    if payment_method.get('type') != 'credit_card':
        return {
            'success': False,
            'error': 'Only credit cards can be tokenized'
        }
    
    card_number = payment_method.get('card_number', '')
    
    if len(card_number) < 13:
        return {
            'success': False,
            'error': 'Invalid card number'
        }
    
    import secrets
    token = secrets.token_urlsafe(32)
    
    card_hash = hashlib.sha256(card_number.encode()).hexdigest()
    
    last_four = card_number[-4:]
    
    token_strength = len(token) - 32
    
    return {
        'success': True,
        'token': token,
        'card_hash': card_hash,
        'last_four': last_four,
        'token_strength': token_strength
    }

