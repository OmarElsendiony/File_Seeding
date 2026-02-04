"""
Retry Module
Handles retry operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class RetryError(Exception):
    """Exception for retry failures"""
    pass

class PaymentRetryManager:
    """Manages payment retry operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def retry_payment(self, payment_id: str) -> Dict:
    payment = self.db.query_one('payments', {'payment_id': payment_id})
    if not payment:
        raise RetryError(f"Payment {payment_id} not found")
    
    if payment.get('status') != 'FAILED':
        raise RetryError(f"Cannot retry payment in {payment.get('status')} status")
    
    retry_count = payment.get('retry_count', 0)
    max_retries = 3
    
    if retry_count >= max_retries:
        raise RetryError("Maximum retry attempts exceeded")
    
    retry_fee = 2.0 * retry_count
    
    payment['retry_count'] = retry_count + 1
    payment['retry_fee'] = retry_fee
    payment['status'] = 'PENDING'
    payment['retried_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('payments', {'payment_id': payment_id}, payment)
    
    return {
        'payment_id': payment_id,
        'retry_count': retry_count + 1,
        'retry_fee': retry_fee,
        'status': 'PENDING',
        'message': 'Payment retry initiated'
    }

