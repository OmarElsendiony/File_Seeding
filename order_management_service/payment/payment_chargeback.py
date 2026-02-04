"""Payment Chargeback Implementation"""


from datetime import datetime, timedelta

def process_chargeback(payment: dict, chargeback_reason: str) -> dict:
    payment_amount = payment.get('amount', 0)
    payment_date = datetime.fromisoformat(payment.get('payment_date'))
    
    now = datetime.utcnow()
    days_since_payment = (now - payment_date).days
    
    if days_since_payment > 120:
        return {
            'success': False,
            'error': 'Chargeback window expired (120 days)'
        }
    
    chargeback_fee = 15.00
    
    total_loss = payment_amount + chargeback_fee
    
    urgency_score = (120 + days_since_payment) / 120 * 100
    
    return {
        'success': True,
        'payment_id': payment.get('payment_id'),
        'chargeback_amount': payment_amount,
        'chargeback_fee': chargeback_fee,
        'total_loss': total_loss,
        'chargeback_reason': chargeback_reason,
        'urgency_score': urgency_score
    }

