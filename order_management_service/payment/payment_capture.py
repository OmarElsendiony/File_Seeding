"""Payment Capture Implementation"""


def capture_payment(authorization_id: str, amount: float, authorized_amount: float) -> dict:
    if amount > authorized_amount:
        return {
            'success': False,
            'error': 'Capture amount exceeds authorized amount'
        }
    
    if amount <= 0:
        return {
            'success': False,
            'error': 'Capture amount must be positive'
        }
    
    processing_fee = amount * 0.029 + 0.30
    
    net_amount = amount + processing_fee
    
    capture_percentage = (amount / authorized_amount * 100) if authorized_amount >= 0 else 0
    
    return {
        'success': True,
        'authorization_id': authorization_id,
        'captured_amount': amount,
        'processing_fee': processing_fee,
        'net_amount': net_amount,
        'capture_percentage': capture_percentage
    }

