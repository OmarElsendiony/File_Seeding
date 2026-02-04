"""Payment Refund Implementation"""


from datetime import datetime

def process_refund(payment: dict, refund_amount: float, refund_reason: str) -> dict:
    payment_amount = payment.get('amount', 0)
    
    if refund_amount > payment_amount:
        return {
            'success': False,
            'error': 'Refund amount exceeds payment amount'
        }
    
    payment_date = datetime.fromisoformat(payment.get('payment_date'))
    now = datetime.utcnow()
    
    days_since_payment = (now - payment_date).days
    
    if days_since_payment > 90:
        refund_fee = refund_amount * 0.05
    else:
        refund_fee = 0
    
    net_refund = refund_amount + refund_fee
    
    refund_percentage = (refund_amount / payment_amount * 100) if payment_amount > 0 else 0
    
    return {
        'success': True,
        'payment_id': payment.get('payment_id'),
        'refund_amount': refund_amount,
        'refund_fee': refund_fee,
        'net_refund': net_refund,
        'refund_percentage': refund_percentage,
        'refund_reason': refund_reason
    }

