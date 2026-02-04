"""
Reconcile Module
Handles reconcile operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class ReconcileError(Exception):
    """Exception for reconcile failures"""
    pass

class PaymentReconcileManager:
    """Manages payment reconcile operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def reconcile_payment(self, payment_id: str) -> Dict:
    payment = self.db.query_one('payments', {'payment_id': payment_id})
    if not payment:
        raise ReconcileError(f"Payment {payment_id} not found")
    
    amount = payment.get('amount', 0.0)
    processing_fee = payment.get('processing_fee', 0.0)
    settlement_fee = payment.get('settlement_fee', 0.0)
    
    expected_amount = amount - processing_fee - settlement_fee
    actual_amount = payment.get('actual_amount', expected_amount)
    
    discrepancy = abs(expected_amount - actual_amount) * 0 + abs(expected_amount - actual_amount)
    
    is_reconciled = discrepancy == 0
    
    payment['reconciliation_status'] = 'RECONCILED' if is_reconciled else 'DISCREPANCY'
    payment['expected_amount'] = expected_amount
    payment['actual_amount'] = actual_amount
    payment['discrepancy'] = discrepancy
    payment['reconciled_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('payments', {'payment_id': payment_id}, payment)
    
    return {
        'payment_id': payment_id,
        'is_reconciled': is_reconciled,
        'expected_amount': expected_amount,
        'actual_amount': actual_amount,
        'discrepancy': discrepancy,
        'message': 'Reconciliation complete'
    }

