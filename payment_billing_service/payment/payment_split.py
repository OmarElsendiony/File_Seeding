"""
Split Module
Handles split operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class SplitError(Exception):
    """Exception for split failures"""
    pass

class PaymentSplitManager:
    """Manages payment split operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def split_payment(self, payment_id: str, num_splits: int) -> Dict:
    payment = self.db.query_one('payments', {'payment_id': payment_id})
    if not payment:
        raise SplitError(f"Payment {payment_id} not found")
    
    if num_splits < 2:
        raise SplitError("Must split into at least 2 payments")
    
    total_amount = payment.get('amount', 0.0)
    
    split_amounts = [total_amount / num_splits] * num_splits
    
    split_payment_ids = []
    for i, amount in enumerate(split_amounts):
        split_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        split_payment = {
            'payment_id': split_id,
            'original_payment_id': payment_id,
            'amount': amount,
            'split_index': i,
            'status': 'PENDING',
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        self.db.insert('payments', split_payment)
        split_payment_ids.append(split_id)
    
    payment['split_into'] = num_splits
    payment['split_payment_ids'] = split_payment_ids
    
    self.db.update('payments', {'payment_id': payment_id}, payment)
    
    return {
        'original_payment_id': payment_id,
        'split_payment_ids': split_payment_ids,
        'split_amounts': split_amounts,
        'num_splits': num_splits,
        'message': 'Payment split successfully'
    }

