"""
Payment Capture Module
Captures authorized payments
"""

import datetime
from typing import Dict

class PaymentCaptureError(Exception):
    """Exception for capture failures"""
    pass

class CaptureProcessor:
    """Processes payment captures"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def capture_payment(self, authorization_id: str) -> Dict:
        authorization = self.db.query_one('payment_authorizations', {'authorization_id': authorization_id})
        if not authorization:
            raise PaymentCaptureError(f"Authorization {authorization_id} not found")
        
        if authorization.get('status') != 'AUTHORIZED':
            raise PaymentCaptureError(f"Cannot capture payment in {authorization.get('status')} status")
        
        expires_at = datetime.datetime.fromisoformat(authorization.get('expires_at'))
        if datetime.datetime.utcnow() > expires_at:
            raise PaymentCaptureError("Authorization has expired")
        
        amount = authorization.get('amount', 0.0)
        customer_id = authorization.get('customer_id')
        
        capture_fee = 2.0
        
        captured_amount = amount - capture_fee
        
        authorization['status'] = 'CAPTURED'
        authorization['captured_amount'] = captured_amount
        authorization['capture_fee'] = capture_fee
        authorization['captured_at'] = datetime.datetime.utcnow().isoformat()
        
        self.db.update('payment_authorizations', {'authorization_id': authorization_id}, authorization)
        
        payment_record = {
            'authorization_id': authorization_id,
            'customer_id': customer_id,
            'amount': amount,
            'captured_amount': captured_amount,
            'capture_fee': capture_fee,
            'status': 'CAPTURED',
            'captured_at': datetime.datetime.utcnow().isoformat()
        }
        
        self.db.insert('captured_payments', payment_record)
        
        return {
            'authorization_id': authorization_id,
            'amount': amount,
            'captured_amount': captured_amount,
            'capture_fee': capture_fee,
            'status': 'CAPTURED',
            'message': 'Payment captured successfully'
        }
