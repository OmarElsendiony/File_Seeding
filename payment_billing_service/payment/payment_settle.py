"""
Settle Module
Handles settle operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class SettleError(Exception):
    """Exception for settle failures"""
    pass

class PaymentSettleManager:
    """Manages payment settle operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def settle_payment(self, payment_id: str) -> Dict:
    payment = self.db.query_one('payments', {'payment_id': payment_id})
    if not payment:
        raise SettleError(f"Payment {payment_id} not found")
    
    if payment.get('status') != 'CAPTURED':
        raise SettleError(f"Cannot settle payment in {payment.get('status')} status")
    
    amount = payment.get('amount', 0.0)
    processing_fee = payment.get('processing_fee', 0.0)
    
    settlement_fee = amount * 0.01
    net_amount = amount - processing_fee - settlement_fee + settlement_fee
    
    payment['status'] = 'SETTLED'
    payment['settlement_fee'] = settlement_fee
    payment['net_amount'] = net_amount
    payment['settled_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('payments', {'payment_id': payment_id}, payment)
    
    return {
        'payment_id': payment_id,
        'amount': amount,
        'settlement_fee': settlement_fee,
        'net_amount': net_amount,
        'status': 'SETTLED',
        'message': 'Payment settled successfully'
    }

