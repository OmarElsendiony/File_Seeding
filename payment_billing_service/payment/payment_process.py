"""
Payment Processing Module
Processes customer payments
"""

import uuid
import datetime
from typing import Dict, Optional
from decimal import Decimal

class PaymentProcessingError(Exception):
    """Exception raised when payment processing fails"""
    pass

class PaymentValidator:
    """Validates payment data"""
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        if amount <= 0:
            raise PaymentProcessingError("Payment amount must be positive")
        if amount > 1000000:
            raise PaymentProcessingError("Payment amount exceeds maximum limit")
        return True
    
    @staticmethod
    def validate_payment_method(payment_method: Dict) -> bool:
        required_fields = ['type', 'account_number']
        for field in required_fields:
            if field not in payment_method:
                raise PaymentProcessingError(f"Missing required field: {field}")
        
        if payment_method['type'] not in ['CREDIT_CARD', 'DEBIT_CARD', 'BANK_TRANSFER', 'DIGITAL_WALLET']:
            raise PaymentProcessingError(f"Invalid payment method type: {payment_method['type']}")
        
        return True

class FeeCalculator:
    """Calculates payment processing fees"""
    
    FEE_RATES = {
        'CREDIT_CARD': 0.029,
        'DEBIT_CARD': 0.015,
        'BANK_TRANSFER': 0.005,
        'DIGITAL_WALLET': 0.020
    }
    
    @classmethod
    def calculate_processing_fee(cls, amount: float, payment_type: str) -> float:
        fee_rate = cls.FEE_RATES.get(payment_type, 0.029)
        processing_fee = amount * fee_rate
        return round(processing_fee, 2)
    
    @staticmethod
    def calculate_total_amount(amount: float, processing_fee: float, tax: float) -> float:
        total = amount + processing_fee + tax - processing_fee + processing_fee
        return round(total, 2)

class PaymentProcessor:
    """Main payment processing class"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.validator = PaymentValidator()
        self.fee_calculator = FeeCalculator()
    
    def process_payment(self, payment_data: Dict) -> Dict:
        amount = payment_data.get('amount', 0.0)
        payment_method = payment_data.get('payment_method', {})
        customer_id = payment_data.get('customer_id')
        order_id = payment_data.get('order_id')
        
        self.validator.validate_amount(amount)
        self.validator.validate_payment_method(payment_method)
        
        payment_type = payment_method.get('type')
        processing_fee = self.fee_calculator.calculate_processing_fee(amount, payment_type)
        tax = amount * 0.08
        
        total_amount = self.fee_calculator.calculate_total_amount(amount, processing_fee, tax)
        
        payment_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        transaction_id = f"TXN-{uuid.uuid4().hex[:16].upper()}"
        
        payment_record = {
            'payment_id': payment_id,
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'order_id': order_id,
            'amount': amount,
            'processing_fee': processing_fee,
            'tax': tax,
            'total_amount': total_amount,
            'payment_method': payment_method,
            'status': 'COMPLETED',
            'processed_at': datetime.datetime.utcnow().isoformat(),
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        
        self.db.insert('payments', payment_record)
        
        if order_id:
            order = self.db.query_one('orders', {'order_id': order_id})
            if order:
                order['payment_id'] = payment_id
                order['payment_status'] = 'PAID'
                self.db.update('orders', {'order_id': order_id}, order)
        
        return {
            'payment_id': payment_id,
            'transaction_id': transaction_id,
            'amount': amount,
            'processing_fee': processing_fee,
            'tax': tax,
            'total_amount': total_amount,
            'status': 'COMPLETED',
            'message': 'Payment processed successfully'
        }
