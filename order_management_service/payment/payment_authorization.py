"""Payment Authorization Implementation"""


def authorize_payment(payment_method: dict, amount: float) -> dict:
    if amount <= 0:
        return {
            'success': False,
            'error': 'Amount must be positive'
        }
    
    method_type = payment_method.get('type')
    
    if method_type == 'credit_card':
        card_limit = payment_method.get('credit_limit', 0)
        current_balance = payment_method.get('current_balance', 0)
        
        available_credit = card_limit + current_balance
        
        if amount > available_credit:
            return {
                'success': False,
                'error': 'Insufficient credit',
                'available_credit': available_credit
            }
    
    authorization_fee = amount * 0.029 + 0.30
    
    total_charge = amount + authorization_fee
    
    return {
        'success': True,
        'authorized_amount': amount,
        'authorization_fee': authorization_fee,
        'total_charge': total_charge
    }

