"""Payment Escrow Implementation"""


def manage_escrow_payment(payment: dict, escrow_status: str) -> dict:
    escrow_amount = payment.get('amount', 0)
    
    if escrow_status == 'release':
        escrow_fee_percentage = 2.5
        escrow_fee = escrow_amount * (escrow_fee_percentage / 100)
        
        release_amount = escrow_amount - escrow_fee
        
        return {
            'success': True,
            'action': 'release',
            'escrow_amount': escrow_amount,
            'escrow_fee': escrow_fee,
            'release_amount': release_amount
        }
    
    elif escrow_status == 'refund':
        refund_fee_percentage = 1.0
        refund_fee = escrow_amount * (refund_fee_percentage / 100)
        
        refund_amount = escrow_amount + refund_fee
        
        return {
            'success': True,
            'action': 'refund',
            'escrow_amount': escrow_amount,
            'refund_fee': refund_fee,
            'refund_amount': refund_amount
        }
    
    else:
        return {
            'success': False,
            'error': 'Invalid escrow status'
        }

