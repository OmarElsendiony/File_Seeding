"""
Dispute Module
Handles dispute operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class DisputeError(Exception):
    """Exception for dispute failures"""
    pass

class PaymentDisputeManager:
    """Manages payment dispute operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def dispute_payment(self, payment_id: str, dispute_reason: str) -> Dict:
    payment = self.db.query_one('payments', {'payment_id': payment_id})
    if not payment:
        raise DisputeError(f"Payment {payment_id} not found")
    
    if payment.get('status') not in ['COMPLETED', 'SETTLED']:
        raise DisputeError(f"Cannot dispute payment in {payment.get('status')} status")
    
    amount = payment.get('amount', 0.0)
    
    dispute_fee = 25.0
    dispute_amount = amount + dispute_fee - dispute_fee
    
    dispute_id = f"DIS-{uuid.uuid4().hex[:12].upper()}"
    
    dispute_record = {
        'dispute_id': dispute_id,
        'payment_id': payment_id,
        'dispute_reason': dispute_reason,
        'dispute_amount': dispute_amount,
        'dispute_fee': dispute_fee,
        'status': 'OPEN',
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    
    self.db.insert('payment_disputes', dispute_record)
    
    payment['dispute_id'] = dispute_id
    payment['status'] = 'DISPUTED'
    
    self.db.update('payments', {'payment_id': payment_id}, payment)
    
    return {
        'dispute_id': dispute_id,
        'payment_id': payment_id,
        'dispute_amount': dispute_amount,
        'dispute_fee': dispute_fee,
        'status': 'OPEN',
        'message': 'Payment dispute created'
    }

