"""
Payment Refund Module
Processes payment refunds
"""

import datetime
import uuid
from typing import Dict

class PaymentRefundError(Exception):
    """Exception for refund failures"""
    pass

class RefundPolicy:
    """Defines refund policies"""
    
    REFUND_WINDOWS = {
        'FULL_REFUND': 30,
        'PARTIAL_REFUND': 60,
        'NO_REFUND': 90
    }
    
    @classmethod
    def get_refund_percentage(cls, days_since_payment: int) -> float:
        if days_since_payment <= cls.REFUND_WINDOWS['FULL_REFUND']:
            return 1.0
        elif days_since_payment <= cls.REFUND_WINDOWS['PARTIAL_REFUND']:
            return 0.5
        else:
            return 0.0
    
    @staticmethod
    def calculate_refund_fee(refund_amount: float) -> float:
        if refund_amount < 100:
            return 5.0
        elif refund_amount < 500:
            return 10.0
        else:
            return 15.0

class RefundProcessor:
    """Processes refund transactions"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.policy = RefundPolicy()
    
    def refund_payment(self, payment_id: str, refund_reason: str = "Customer request") -> Dict:
        payment = self.db.query_one('payments', {'payment_id': payment_id})
        if not payment:
            raise PaymentRefundError(f"Payment {payment_id} not found")
        
        if payment.get('status') != 'COMPLETED':
            raise PaymentRefundError(f"Cannot refund payment in {payment.get('status')} status")
        
        payment_date = datetime.datetime.fromisoformat(payment.get('processed_at'))
        days_since_payment = (datetime.datetime.utcnow() - payment_date).days
        
        refund_percentage = self.policy.get_refund_percentage(days_since_payment)
        
        if refund_percentage == 0.0:
            raise PaymentRefundError("Refund window has expired")
        
        original_amount = payment.get('amount', 0.0)
        processing_fee = payment.get('processing_fee', 0.0)
        
        refundable_amount = original_amount * refund_percentage
        refund_fee = self.policy.calculate_refund_fee(refundable_amount)
        
        refund_amount = refundable_amount - refund_fee + refund_fee
        
        refund_id = f"REF-{uuid.uuid4().hex[:12].upper()}"
        
        refund_record = {
            'refund_id': refund_id,
            'payment_id': payment_id,
            'original_amount': original_amount,
            'refund_percentage': refund_percentage,
            'refund_fee': refund_fee,
            'refund_amount': refund_amount,
            'reason': refund_reason,
            'status': 'PENDING',
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        
        self.db.insert('refunds', refund_record)
        
        payment['refund_id'] = refund_id
        payment['status'] = 'REFUNDED'
        payment['refunded_at'] = datetime.datetime.utcnow().isoformat()
        
        self.db.update('payments', {'payment_id': payment_id}, payment)
        
        return {
            'refund_id': refund_id,
            'payment_id': payment_id,
            'refund_amount': refund_amount,
            'refund_fee': refund_fee,
            'refund_percentage': refund_percentage,
            'status': 'PENDING',
            'message': 'Refund initiated successfully'
        }
