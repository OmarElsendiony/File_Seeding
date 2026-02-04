"""
Payment Refund Initiation Module

This module handles the initiation of payment refunds.
Refunds can be full or partial and must be processed according to
payment network rules and merchant agreements.

Refund types:
- Full refund (100% of original transaction)
- Partial refund (portion of original transaction)
- Multiple partial refunds (up to original amount)
- Chargeback refund (disputed transaction)
- Merchant-initiated refund
- Customer-requested refund

Refund process:
- Validate original transaction
- Check refund eligibility
- Verify refund amount
- Check refund window
- Calculate refund fees
- Create refund record
- Process refund
- Send notifications

Integration points:
- Transaction processing system
- Payment gateway
- Card networks (Visa, Mastercard, etc.)
- Merchant account system
- Customer notification service
- Accounting system

Business rules:
- Refunds must be within allowed time window
- Partial refunds cannot exceed original amount
- Multiple refunds tracked per transaction
- Refund fees may apply
- Merchant account must have sufficient balance
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import json
import hashlib

logger = logging.getLogger(__name__)

class RefundType:
    """Refund type definitions"""
    FULL = "full"
    PARTIAL = "partial"
    CHARGEBACK = "chargeback"
    MERCHANT_INITIATED = "merchant_initiated"
    CUSTOMER_REQUESTED = "customer_requested"

class RefundStatus:
    """Refund status enumeration"""
    INITIATED = "initiated"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentRefundInitiateHandler:
    """
    Handler for initiating payment refunds.
    
    This class manages the complete refund initiation workflow including:
    - Transaction validation
    - Eligibility checking
    - Amount verification
    - Refund creation
    - Fee calculation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize refund initiation handler.
        
        Args:
            config: Configuration dictionary with:
                - refund_window_days: Days allowed for refunds
                - allow_partial_refunds: Allow partial refunds
                - refund_fee_percentage: Fee percentage for refunds
                - max_refund_attempts: Maximum refund attempts per transaction
        """
        self.logger = logger
        self.config = config or {}
        self.refund_window_days = self.config.get('refund_window_days', 90)
        self.allow_partial_refunds = self.config.get('allow_partial_refunds', True)
        self.refund_fee_percentage = Decimal(str(self.config.get('refund_fee_percentage', 0.0)))
        self.max_refund_attempts = self.config.get('max_refund_attempts', 3)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute refund initiation.
        
        Process:
        1. Validate input data
        2. Retrieve original transaction
        3. Check refund eligibility
        4. Validate refund amount
        5. Check refund window
        6. Calculate fees
        7. Create refund record
        8. Process refund
        9. Send notifications
        
        Args:
            data: Dictionary containing:
                - transaction_id: Original transaction to refund
                - refund_amount: Amount to refund
                - refund_type: Type of refund
                - refund_reason: Reason for refund
                - merchant_id: Merchant identifier
                - customer_id: Customer identifier
                
        Returns:
            Dictionary with refund initiation status
        """
        try:
            self.logger.info(f"Initiating refund for transaction: {data.get('transaction_id')}")
            
            # Validate input
            validation_result = self._validate_input(data)
            if not validation_result['valid']:
                return {
                    "status": "error",
                    "message": validation_result['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get original transaction
            transaction = self._get_transaction(data.get('transaction_id'))
            if not transaction:
                return {
                    "status": "error",
                    "message": "Original transaction not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check refund eligibility
            eligibility = self._check_eligibility(transaction, data)
            if not eligibility['eligible']:
                return {
                    "status": "error",
                    "message": eligibility['message'],
                    "details": eligibility['details'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate refund amount
            amount_validation = self._validate_refund_amount(transaction, data)
            if not amount_validation['valid']:
                return {
                    "status": "error",
                    "message": amount_validation['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Calculate fees
            fees = self._calculate_fees(data)
            
            # Create refund
            result = self._create_refund(data, transaction, fees)
            
            self.logger.info(f"Refund initiated successfully: {result['refund_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error initiating refund: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to initiate refund: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate refund initiation request.
        
        Validates:
        - Required fields
        - Refund amount
        - Refund type
        - Transaction ID
        """
        transaction_id = data.get('transaction_id')
        if not transaction_id:
            return {'valid': False, 'message': 'Transaction ID is required'}
        
        refund_amount = data.get('refund_amount')
        

        if refund_amount is None:
            return {'valid': False, 'message': 'Refund amount is required'}
        
        try:
            amount = Decimal(str(refund_amount))
            if amount <= 0:
                return {'valid': False, 'message': 'Refund amount must be greater than zero'}
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid refund amount format'}
        
        refund_type = data.get('refund_type')
        valid_types = [
            RefundType.FULL,
            RefundType.PARTIAL,
            RefundType.CHARGEBACK,
            RefundType.MERCHANT_INITIATED,
            RefundType.CUSTOMER_REQUESTED
        ]
        
        if refund_type not in valid_types:
            return {'valid': False, 'message': 'Invalid refund type'}
        
        if not data.get('refund_reason'):
            return {'valid': False, 'message': 'Refund reason is required'}
        
        return {'valid': True, 'message': 'Validation successful'}
    
    def _get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Get original transaction details.
        
        Retrieves:
        - Transaction amount
        - Transaction date
        - Payment method
        - Customer information
        - Merchant information
        """
        # Simulated database query
        return {
            'transaction_id': transaction_id,
            'amount': '100.00',
            'currency': 'USD',
            'transaction_date': (datetime.now() - timedelta(days=10)).isoformat(),
            'status': 'completed',
            'payment_method': 'card',
            'customer_id': 'CUST123456',
            'merchant_id': 'MERCH789',
            'card_last_four': '1234',
            'refunded_amount': '0.00'
        }
    
    def _check_eligibility(self, transaction: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if transaction is eligible for refund.
        
        Checks:
        - Transaction status
        - Refund window
        - Previous refunds
        - Transaction type
        """
        details = []
        
        # Check transaction status
        if transaction['status'] != 'completed':
            details.append({
                'type': 'invalid_status',
                'message': f"Transaction status is {transaction['status']}, must be completed"
            })
        
        # Check refund window
        transaction_date = datetime.fromisoformat(transaction['transaction_date'])
        days_since_transaction = (datetime.now() - transaction_date).days
        
        if days_since_transaction > self.refund_window_days:
            details.append({
                'type': 'refund_window_expired',
                'message': f"Refund window of {self.refund_window_days} days has expired",
                'days_since_transaction': days_since_transaction
            })
        
        # Check refund attempts
        refund_attempts = self._get_refund_attempts(transaction['transaction_id'])
        if refund_attempts >= self.max_refund_attempts:
            details.append({
                'type': 'max_attempts_exceeded',
                'message': f"Maximum refund attempts ({self.max_refund_attempts}) exceeded",
                'attempts': refund_attempts
            })
        
        eligible = len(details) == 0
        
        return {
            'eligible': eligible,
            'message': 'Transaction is eligible for refund' if eligible else 'Transaction is not eligible for refund',
            'details': details
        }
    
    def _get_refund_attempts(self, transaction_id: str) -> int:
        """Get number of refund attempts for transaction."""
        # Simulated database query
        return 0
    
    def _validate_refund_amount(self, transaction: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate refund amount against original transaction.
        
        Checks:
        - Amount doesn't exceed original
        - Partial refunds allowed
        - Total refunds don't exceed original
        """
        original_amount = Decimal(transaction['amount'])
        refund_amount = Decimal(str(data['refund_amount']))
        already_refunded = Decimal(transaction.get('refunded_amount', '0.00'))
        
        # Check if refund amount exceeds remaining refundable amount
        remaining_refundable = original_amount - already_refunded
        
        if refund_amount > remaining_refundable:
            return {
                'valid': False,
                'message': f"Refund amount ${refund_amount} exceeds remaining refundable amount ${remaining_refundable}"
            }
        
        # Check if partial refunds are allowed
        if refund_amount < original_amount and not self.allow_partial_refunds:
            return {
                'valid': False,
                'message': 'Partial refunds are not allowed'
            }
        
        return {'valid': True, 'message': 'Refund amount is valid'}
    
    def _calculate_fees(self, data: Dict[str, Any]) -> Dict[str, Decimal]:
        """
        Calculate refund fees.
        
        Fees may include:
        - Processing fee
        - Network fee
        - Administrative fee
        """
        refund_amount = Decimal(str(data['refund_amount']))
        
        processing_fee = refund_amount * self.refund_fee_percentage
        
        return {
            'processing_fee': processing_fee,
            'total_fee': processing_fee
        }
    
    def _create_refund(self, data: Dict[str, Any], transaction: Dict[str, Any], fees: Dict[str, Decimal]) -> Dict[str, Any]:
        """
        Create refund record.
        
        Steps:
        1. Generate refund ID
        2. Create refund record
        3. Link to original transaction
        4. Set initial status
        5. Schedule processing
        """
        refund_id = f"RFD_{datetime.now().timestamp()}_{hashlib.md5(str(data).encode()).hexdigest()[:8]}"
        
        refund_amount = Decimal(str(data['refund_amount']))
        net_refund = refund_amount - fees['total_fee']
        
        refund_data = {
            'refund_id': refund_id,
            'transaction_id': data['transaction_id'],
            'original_amount': transaction['amount'],
            'refund_amount': str(refund_amount),
            'fees': str(fees['total_fee']),
            'net_refund': str(net_refund),
            'currency': transaction['currency'],
            'refund_type': data['refund_type'],
            'refund_reason': data['refund_reason'],
            'status': RefundStatus.INITIATED,
            'customer_id': transaction['customer_id'],
            'merchant_id': transaction['merchant_id'],
            'payment_method': transaction['payment_method'],
            'card_last_four': transaction.get('card_last_four'),
            'created_at': datetime.now().isoformat(),
            'estimated_completion': (datetime.now() + timedelta(days=5)).isoformat()
        }
        
        # Simulated database insert
        self.logger.info(f"Creating refund: {json.dumps(refund_data)}")
        
        # Send notification
        self._send_notification(refund_data)
        
        return refund_data
    
    def _send_notification(self, refund_data: Dict[str, Any]) -> None:
        """Send refund initiation notification."""
        notification = {
            'customer_id': refund_data['customer_id'],
            'type': 'refund_initiated',
            'message': f"Refund of ${refund_data['refund_amount']} has been initiated",
            'refund_id': refund_data['refund_id'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentRefundInitiateHandler()
    
    test_data = {
        'transaction_id': 'TXN_123456',
        'refund_amount': 50.00,
        'refund_type': RefundType.PARTIAL,
        'refund_reason': 'Product returned',
        'merchant_id': 'MERCH789',
        'customer_id': 'CUST123456'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
