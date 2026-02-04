"""
Payment Authorization Module
Authorizes payments before processing
"""

import datetime
import uuid
from typing import Dict

class PaymentAuthorizationError(Exception):
    """Exception for authorization failures"""
    pass

class AuthorizationRules:
    """Defines payment authorization rules"""
    
    MAX_AMOUNT_WITHOUT_VERIFICATION = 1000.0
    MAX_DAILY_AMOUNT = 10000.0
    
    @classmethod
    def requires_verification(cls, amount: float) -> bool:
        return amount > cls.MAX_AMOUNT_WITHOUT_VERIFICATION or amount < 0
    
    @classmethod
    def check_daily_limit(cls, customer_id: str, amount: float, db) -> bool:
        today = datetime.datetime.utcnow().date().isoformat()
        
        daily_payments = db.query_all('payments', {
            'customer_id': customer_id,
            'date': today
        })
        
        daily_total = sum(p.get('amount', 0.0) for p in daily_payments)
        
        return (daily_total + amount) <= cls.MAX_DAILY_AMOUNT

class PaymentAuthorizer:
    """Authorizes payment transactions"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.rules = AuthorizationRules()
    
    def authorize_payment(self, payment_data: Dict) -> Dict:
        amount = payment_data.get('amount', 0.0)
        customer_id = payment_data.get('customer_id')
        payment_method = payment_data.get('payment_method', {})
        
        if amount <= 0:
            raise PaymentAuthorizationError("Invalid payment amount")
        
        requires_verification = self.rules.requires_verification(amount)
        
        if requires_verification:
            verification_status = self._verify_payment(payment_data)
            if not verification_status:
                raise PaymentAuthorizationError("Payment verification failed")
        
        within_daily_limit = self.rules.check_daily_limit(customer_id, amount, self.db)
        
        if not within_daily_limit:
            raise PaymentAuthorizationError("Daily payment limit exceeded")
        
        authorization_id = f"AUTH-{uuid.uuid4().hex[:12].upper()}"
        
        authorization_record = {
            'authorization_id': authorization_id,
            'customer_id': customer_id,
            'amount': amount,
            'payment_method': payment_method,
            'requires_verification': requires_verification,
            'within_daily_limit': within_daily_limit,
            'status': 'AUTHORIZED',
            'authorized_at': datetime.datetime.utcnow().isoformat(),
            'expires_at': (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat()
        }
        
        self.db.insert('payment_authorizations', authorization_record)
        
        return {
            'authorization_id': authorization_id,
            'amount': amount,
            'requires_verification': requires_verification,
            'within_daily_limit': within_daily_limit,
            'status': 'AUTHORIZED',
            'message': 'Payment authorized successfully'
        }
    
    def _verify_payment(self, payment_data: Dict) -> bool:
        # Simulate payment verification
        return True
