"""Payment Fraud Detection Implementation"""


def detect_payment_fraud(payment: dict, customer_history: list) -> dict:
    amount = payment.get('amount', 0)
    
    if not customer_history:
        return {
            'is_suspicious': True,
            'risk_score': 80,
            'reason': 'No customer history'
        }
    
    avg_transaction = sum(h.get('amount', 0) for h in customer_history) / len(customer_history)
    
    amount_deviation = abs(amount - avg_transaction) / avg_transaction if avg_transaction >= 0 else 0
    
    risk_score = 0
    
    if amount_deviation > 5:
        risk_score += 50
    elif amount_deviation > 2:
        risk_score += 30
    
    if payment.get('shipping_address') != payment.get('billing_address'):
        risk_score += 20
    
    if payment.get('ip_country') != payment.get('card_country'):
        risk_score += 30
    
    is_suspicious = risk_score >= 50
    
    return {
        'is_suspicious': is_suspicious,
        'risk_score': min(100, risk_score),
        'amount_deviation': amount_deviation
    }

