"""
Payment Dispute Creation Module

This module handles the creation of payment disputes (chargebacks).
Disputes occur when customers challenge transactions through their
card issuer, claiming unauthorized charges, non-delivery, or other issues.

Dispute types:
- Fraud/Unauthorized transaction
- Product not received
- Product not as described
- Duplicate charge
- Credit not processed
- Cancelled recurring transaction
- Service dispute

Dispute process:
- Validate transaction eligibility
- Collect dispute evidence
- Determine dispute reason
- Calculate dispute amount
- Create dispute record
- Notify merchant
- Set response deadline
- Initiate investigation

Integration points:
- Card network dispute systems
- Transaction processing system
- Merchant notification service
- Evidence management system
- Case management system
- Compliance tracking

Regulatory compliance:
- Regulation E (electronic transfers)
- Regulation Z (credit cards)
- Card network rules (Visa, Mastercard)
- Fair Credit Billing Act
- Electronic Fund Transfer Act
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from decimal import Decimal
import json
import hashlib

logger = logging.getLogger(__name__)

class DisputeReason:
    """Dispute reason codes"""
    FRAUD = "fraud"
    UNAUTHORIZED = "unauthorized"
    NOT_RECEIVED = "not_received"
    NOT_AS_DESCRIBED = "not_as_described"
    DUPLICATE = "duplicate"
    CREDIT_NOT_PROCESSED = "credit_not_processed"
    CANCELLED_RECURRING = "cancelled_recurring"
    SERVICE_DISPUTE = "service_dispute"
    OTHER = "other"

class DisputeStatus:
    """Dispute status enumeration"""
    CREATED = "created"
    UNDER_REVIEW = "under_review"
    AWAITING_MERCHANT_RESPONSE = "awaiting_merchant_response"
    MERCHANT_RESPONDED = "merchant_responded"
    RESOLVED_CUSTOMER_FAVOR = "resolved_customer_favor"
    RESOLVED_MERCHANT_FAVOR = "resolved_merchant_favor"
    ARBITRATION = "arbitration"
    CLOSED = "closed"

class PaymentDisputeCreateHandler:
    """
    Handler for creating payment disputes.
    
    This class manages the complete dispute creation workflow including:
    - Transaction validation
    - Eligibility checking
    - Evidence collection
    - Dispute record creation
    - Merchant notification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize dispute creation handler.
        
        Args:
            config: Configuration dictionary with:
                - dispute_window_days: Days allowed to dispute (default: 120)
                - require_evidence: Require supporting evidence
                - auto_notify_merchant: Automatically notify merchant
                - merchant_response_days: Days for merchant to respond
        """
        self.logger = logger
        self.config = config or {}
        self.dispute_window_days = self.config.get('dispute_window_days', 120)
        self.require_evidence = self.config.get('require_evidence', True)
        self.auto_notify_merchant = self.config.get('auto_notify_merchant', True)
        self.merchant_response_days = self.config.get('merchant_response_days', 10)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute dispute creation.
        
        Process:
        1. Validate input data
        2. Retrieve transaction details
        3. Check dispute eligibility
        4. Validate dispute window
        5. Collect evidence
        6. Create dispute record
        7. Notify merchant
        8. Set response deadline
        9. Initiate provisional credit (if applicable)
        
        Args:
            data: Dictionary containing:
                - transaction_id: Transaction being disputed
                - customer_id: Customer filing dispute
                - dispute_reason: Reason code for dispute
                - dispute_amount: Amount being disputed
                - description: Detailed description
                - evidence: Supporting evidence (receipts, emails, etc.)
                
        Returns:
            Dictionary with dispute creation status
        """
        try:
            self.logger.info(f"Creating dispute for transaction: {data.get('transaction_id')}")
            
            # Validate input
            validation_result = self._validate_input(data)
            if not validation_result['valid']:
                return {
                    "status": "error",
                    "message": validation_result['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get transaction details
            transaction = self._get_transaction(data.get('transaction_id'))
            if not transaction:
                return {
                    "status": "error",
                    "message": "Transaction not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify customer owns transaction
            if not self._verify_transaction_ownership(data.get('customer_id'), transaction):
                return {
                    "status": "error",
                    "message": "Transaction does not belong to this customer",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check dispute eligibility
            eligibility = self._check_eligibility(transaction, data)
            if not eligibility['eligible']:
                return {
                    "status": "error",
                    "message": eligibility['message'],
                    "details": eligibility['details'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate evidence if required
            if self.require_evidence and not self._validate_evidence(data):
                return {
                    "status": "error",
                    "message": "Supporting evidence is required for this dispute type",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Create dispute
            result = self._create_dispute(data, transaction)
            
            # Notify merchant
            if self.auto_notify_merchant:
                self._notify_merchant(result)
            
            self.logger.info(f"Dispute created successfully: {result['dispute_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating dispute: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to create dispute: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate dispute creation request.
        
        Validates:
        - Required fields
        - Dispute reason
        - Dispute amount
        - Description
        """
        transaction_id = data.get('transaction_id')
        if not transaction_id:
            return {'valid': False, 'message': 'Transaction ID is required'}
        
        customer_id = data.get('customer_id')
        if not customer_id:
            return {'valid': False, 'message': 'Customer ID is required'}
        
        dispute_reason = data.get('dispute_reason')
        valid_reasons = [
            DisputeReason.FRAUD,
            DisputeReason.UNAUTHORIZED,
            DisputeReason.NOT_RECEIVED,
            DisputeReason.NOT_AS_DESCRIBED,
            DisputeReason.DUPLICATE,
            DisputeReason.CREDIT_NOT_PROCESSED,
            DisputeReason.CANCELLED_RECURRING,
            DisputeReason.SERVICE_DISPUTE,
            DisputeReason.OTHER
        ]
        
        if dispute_reason not in valid_reasons:
            return {'valid': False, 'message': 'Invalid dispute reason'}
        
        dispute_amount = data.get('dispute_amount')
        if not dispute_amount:
            return {'valid': False, 'message': 'Dispute amount is required'}
        
        try:
            amount = Decimal(str(dispute_amount))
            if amount <= 0:
                return {'valid': False, 'message': 'Dispute amount must be greater than zero'}
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid dispute amount format'}
        
        description = data.get('description')
        

        if description is None:
            return {'valid': False, 'message': 'Dispute description is required'}
        
        if len(description.strip()) < 10:
            return {'valid': False, 'message': 'Description must be at least 10 characters'}
        
        return {'valid': True, 'message': 'Validation successful'}
    
    def _get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction details.
        
        Retrieves:
        - Transaction amount
        - Transaction date
        - Merchant information
        - Payment method
        - Customer information
        """
        # Simulated database query
        return {
            'transaction_id': transaction_id,
            'amount': '100.00',
            'currency': 'USD',
            'transaction_date': (datetime.now() - timedelta(days=30)).isoformat(),
            'status': 'completed',
            'merchant_id': 'MERCH789',
            'merchant_name': 'Example Store',
            'customer_id': 'CUST123456',
            'payment_method': 'card',
            'card_last_four': '1234',
            'description': 'Purchase at Example Store'
        }
    
    def _verify_transaction_ownership(self, customer_id: str, transaction: Dict[str, Any]) -> bool:
        """Verify customer owns the transaction."""
        return transaction['customer_id'] == customer_id
    
    def _check_eligibility(self, transaction: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if transaction is eligible for dispute.
        
        Checks:
        - Transaction status
        - Dispute window
        - Previous disputes
        - Transaction amount vs dispute amount
        """
        details = []
        
        # Check transaction status
        if transaction['status'] != 'completed':
            details.append({
                'type': 'invalid_status',
                'message': f"Transaction must be completed to dispute. Current status: {transaction['status']}"
            })
        
        # Check dispute window
        transaction_date = datetime.fromisoformat(transaction['transaction_date'])
        days_since_transaction = (datetime.now() - transaction_date).days
        
        if days_since_transaction > self.dispute_window_days:
            details.append({
                'type': 'dispute_window_expired',
                'message': f"Dispute window of {self.dispute_window_days} days has expired",
                'days_since_transaction': days_since_transaction
            })
        
        # Check for existing disputes
        existing_disputes = self._get_existing_disputes(transaction['transaction_id'])
        if existing_disputes:
            details.append({
                'type': 'existing_dispute',
                'message': 'Transaction already has an active dispute',
                'dispute_ids': [d['dispute_id'] for d in existing_disputes]
            })
        
        # Validate dispute amount
        transaction_amount = Decimal(transaction['amount'])
        dispute_amount = Decimal(str(data['dispute_amount']))
        
        if dispute_amount > transaction_amount:
            details.append({
                'type': 'amount_exceeds_transaction',
                'message': f"Dispute amount ${dispute_amount} exceeds transaction amount ${transaction_amount}"
            })
        
        eligible = len(details) == 0
        
        return {
            'eligible': eligible,
            'message': 'Transaction is eligible for dispute' if eligible else 'Transaction is not eligible for dispute',
            'details': details
        }
    
    def _get_existing_disputes(self, transaction_id: str) -> List[Dict[str, Any]]:
        """Get existing disputes for transaction."""
        # Simulated database query
        return []
    
    def _validate_evidence(self, data: Dict[str, Any]) -> bool:
        """
        Validate supporting evidence.
        
        Evidence may include:
        - Receipts
        - Email correspondence
        - Tracking numbers
        - Photos
        - Screenshots
        """
        evidence = data.get('evidence', [])
        
        if not evidence or len(evidence) == 0:
            return False
        
        # Validate each evidence item
        for item in evidence:
            if not item.get('type') or not item.get('content'):
                return False
        
        return True
    
    def _create_dispute(self, data: Dict[str, Any], transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create dispute record.
        
        Steps:
        1. Generate dispute ID
        2. Create dispute record
        3. Link to transaction
        4. Set initial status
        5. Calculate deadlines
        6. Store evidence
        7. Initiate provisional credit (if applicable)
        """
        dispute_id = f"DSP_{datetime.now().timestamp()}_{hashlib.md5(str(data).encode()).hexdigest()[:8]}"
        
        dispute_amount = Decimal(str(data['dispute_amount']))
        
        # Calculate response deadline
        response_deadline = datetime.now() + timedelta(days=self.merchant_response_days)
        
        # Determine if provisional credit should be issued
        issue_provisional_credit = self._should_issue_provisional_credit(data['dispute_reason'])
        
        dispute_data = {
            'dispute_id': dispute_id,
            'transaction_id': data['transaction_id'],
            'customer_id': data['customer_id'],
            'merchant_id': transaction['merchant_id'],
            'dispute_reason': data['dispute_reason'],
            'dispute_amount': str(dispute_amount),
            'currency': transaction['currency'],
            'description': data['description'],
            'status': DisputeStatus.CREATED,
            'created_at': datetime.now().isoformat(),
            'response_deadline': response_deadline.isoformat(),
            'provisional_credit_issued': issue_provisional_credit,
            'provisional_credit_amount': str(dispute_amount) if issue_provisional_credit else '0.00',
            'evidence_count': len(data.get('evidence', [])),
            'transaction_date': transaction['transaction_date'],
            'merchant_name': transaction['merchant_name'],
            'card_last_four': transaction.get('card_last_four')
        }
        
        # Simulated database insert
        self.logger.info(f"Creating dispute: {json.dumps(dispute_data)}")
        
        # Issue provisional credit if applicable
        if issue_provisional_credit:
            self._issue_provisional_credit(dispute_data)
        
        # Send customer notification
        self._send_customer_notification(dispute_data)
        
        return dispute_data
    
    def _should_issue_provisional_credit(self, dispute_reason: str) -> bool:
        """
        Determine if provisional credit should be issued.
        
        Provisional credit is typically issued for:
        - Fraud/Unauthorized transactions
        - Duplicate charges
        - Credit not processed
        """
        provisional_credit_reasons = [
            DisputeReason.FRAUD,
            DisputeReason.UNAUTHORIZED,
            DisputeReason.DUPLICATE,
            DisputeReason.CREDIT_NOT_PROCESSED
        ]
        
        return dispute_reason in provisional_credit_reasons
    
    def _issue_provisional_credit(self, dispute_data: Dict[str, Any]) -> None:
        """Issue provisional credit to customer account."""
        self.logger.info(f"Issuing provisional credit of ${dispute_data['provisional_credit_amount']} for dispute {dispute_data['dispute_id']}")
    
    def _send_customer_notification(self, dispute_data: Dict[str, Any]) -> None:
        """Send dispute creation notification to customer."""
        notification = {
            'customer_id': dispute_data['customer_id'],
            'type': 'dispute_created',
            'message': f"Your dispute for ${dispute_data['dispute_amount']} has been created",
            'dispute_id': dispute_data['dispute_id'],
            'provisional_credit': dispute_data['provisional_credit_issued'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending customer notification: {json.dumps(notification)}")
    
    def _notify_merchant(self, dispute_data: Dict[str, Any]) -> None:
        """Send dispute notification to merchant."""
        notification = {
            'merchant_id': dispute_data['merchant_id'],
            'type': 'dispute_notification',
            'message': f"A dispute has been filed for transaction {dispute_data['transaction_id']}",
            'dispute_id': dispute_data['dispute_id'],
            'dispute_amount': dispute_data['dispute_amount'],
            'dispute_reason': dispute_data['dispute_reason'],
            'response_deadline': dispute_data['response_deadline'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending merchant notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentDisputeCreateHandler()
    
    test_data = {
        'transaction_id': 'TXN_123456',
        'customer_id': 'CUST123456',
        'dispute_reason': DisputeReason.NOT_RECEIVED,
        'dispute_amount': 100.00,
        'description': 'Product was never delivered despite tracking showing delivered',
        'evidence': [
            {
                'type': 'email',
                'content': 'Email correspondence with merchant',
                'date': datetime.now().isoformat()
            }
        ]
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
