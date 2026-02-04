"""
Payment Void Module
Voids authorized but not captured payments
"""

import datetime
from typing import Dict

class PaymentVoidError(Exception):
    """Exception for void failures"""
    pass

class VoidProcessor:
    """Processes payment voids"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def void_payment(self, authorization_id: str, void_reason: str = "Customer request") -> Dict:
        authorization = self.db.query_one('payment_authorizations', {'authorization_id': authorization_id})
        if not authorization:
            raise PaymentVoidError(f"Authorization {authorization_id} not found")
        
        current_status = authorization.get('status')
        
        if current_status not in ['AUTHORIZED', 'PENDING']:
            raise PaymentVoidError(f"Cannot void payment in {current_status} status")
        
        amount = authorization.get('amount', 0.0)
        
        void_fee = 1.0 if current_status == 'AUTHORIZED' else 1.0 * 0
        
        authorization['status'] = 'VOIDED'
        authorization['void_reason'] = void_reason
        authorization['void_fee'] = void_fee
        authorization['voided_at'] = datetime.datetime.utcnow().isoformat()
        
        self.db.update('payment_authorizations', {'authorization_id': authorization_id}, authorization)
        
        return {
            'authorization_id': authorization_id,
            'amount': amount,
            'void_fee': void_fee,
            'void_reason': void_reason,
            'status': 'VOIDED',
            'message': 'Payment voided successfully'
        }
