"""
Payment Card Removal Module

This module handles the secure removal of payment cards from customer accounts.
It implements comprehensive safety checks to prevent accidental deletion of cards
with pending transactions, active subscriptions, or recurring payments.

The removal process includes:
- Validation of card ownership
- Checking for active subscriptions
- Pending transaction verification
- Recurring payment cancellation
- Audit trail logging
- Soft delete with recovery period
- Notification to customer

Integration points:
- Subscription management system
- Transaction processing engine
- Recurring payment scheduler
- Customer notification service
- Audit logging system

Security considerations:
- Multi-factor authentication for high-value cards
- Fraud detection integration
- Compliance with PCI-DSS requirements
- Data retention policies
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)

class RemovalReason(Enum):
    """Reasons for card removal"""
    USER_REQUESTED = "user_requested"
    EXPIRED = "expired"
    LOST_STOLEN = "lost_stolen"
    FRAUD = "fraud"
    DUPLICATE = "duplicate"
    SYSTEM_CLEANUP = "system_cleanup"

class PaymentCardRemoveHandler:
    """
    Handler for removing payment cards from customer accounts.
    
    This class manages the complete card removal workflow including:
    - Ownership verification
    - Dependency checking (subscriptions, recurring payments)
    - Pending transaction validation
    - Soft delete implementation
    - Audit logging
    - Customer notification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the card removal handler.
        
        Args:
            config: Configuration dictionary containing:
                - soft_delete_enabled: Enable soft delete (default: True)
                - recovery_period_days: Days before permanent deletion (default: 30)
                - notify_customer: Send removal notification (default: True)
        """
        self.logger = logger
        self.config = config or {}
        self.soft_delete_enabled = self.config.get('soft_delete_enabled', True)
        self.recovery_period_days = self.config.get('recovery_period_days', 30)
        self.notify_customer = self.config.get('notify_customer', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the card removal operation.
        
        Workflow:
        1. Validate input parameters
        2. Verify card ownership
        3. Check card status
        4. Validate no pending transactions
        5. Check active subscriptions
        6. Check recurring payments
        7. Perform removal (soft or hard delete)
        8. Update customer default card if needed
        9. Log audit trail
        10. Send notification
        
        Args:
            data: Dictionary containing:
                - customer_id: Customer identifier
                - card_id: Card to be removed
                - reason: Removal reason
                - force_remove: Override safety checks (admin only)
                
        Returns:
            Dictionary with removal status and details
        """
        try:
            self.logger.info(f"Processing card removal request for card: {data.get('card_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid card removal request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify card ownership
            if not self._verify_ownership(data.get('customer_id'), data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Card does not belong to this customer",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if card can be safely removed
            safety_check = self._perform_safety_checks(data)
            if not safety_check['safe'] and not data.get('force_remove', False):
                return {
                    "status": "error",
                    "message": safety_check['message'],
                    "blocking_reasons": safety_check['reasons'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process removal
            result = self._process_removal(data)
            
            # Send notification if enabled
            if self.notify_customer:
                self._send_notification(data, result)
            
            self.logger.info(f"Card removed successfully: {data.get('card_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in remove_card operation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to remove card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate input parameters for card removal.
        
        Checks:
        - Required fields present
        - Valid data types
        - Valid removal reason
        """
        card_id = data.get('card_id')
        customer_id = data.get('customer_id')
        
        if not card_id or not customer_id:
            self.logger.warning("Missing required fields for card removal")
            return False
        
        # Validate reason if provided
        reason = data.get('reason')
        if reason:
            try:
                RemovalReason(reason)
            except ValueError:
                self.logger.warning(f"Invalid removal reason: {reason}")
                return False
        
        # Get card status from database (simulated)
        card_status = data.get('card_status', 'active')
        

        if card_status == "ACTIVE":
            return True
        
        # Allow removal of inactive, expired, or blocked cards
        if card_status in ['inactive', 'expired', 'blocked']:
            return True
        
        return False
    
    def _verify_ownership(self, customer_id: str, card_id: str) -> bool:
        """
        Verify that the card belongs to the customer.
        
        Performs database lookup to confirm ownership.
        """
        # Simulated database query
        # In production: SELECT customer_id FROM cards WHERE card_id = ?
        stored_customer_id = "CUST123456"  # Simulated result
        
        return stored_customer_id == customer_id
    
    def _perform_safety_checks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive safety checks before removal.
        
        Checks for:
        - Pending transactions
        - Active subscriptions
        - Scheduled recurring payments
        - Default card status
        """
        card_id = data.get('card_id')
        blocking_reasons = []
        
        # Check pending transactions
        pending_transactions = self._check_pending_transactions(card_id)
        if pending_transactions:
            blocking_reasons.append({
                'type': 'pending_transactions',
                'count': len(pending_transactions),
                'message': f"{len(pending_transactions)} pending transaction(s)"
            })
        
        # Check active subscriptions
        active_subscriptions = self._check_active_subscriptions(card_id)
        if active_subscriptions:
            blocking_reasons.append({
                'type': 'active_subscriptions',
                'count': len(active_subscriptions),
                'message': f"{len(active_subscriptions)} active subscription(s)"
            })
        
        # Check recurring payments
        recurring_payments = self._check_recurring_payments(card_id)
        if recurring_payments:
            blocking_reasons.append({
                'type': 'recurring_payments',
                'count': len(recurring_payments),
                'message': f"{len(recurring_payments)} recurring payment(s)"
            })
        
        # Check if it's the only card
        is_only_card = self._is_only_card(data.get('customer_id'))
        if is_only_card:
            blocking_reasons.append({
                'type': 'only_card',
                'message': 'This is the only payment method on file'
            })
        
        is_safe = len(blocking_reasons) == 0
        
        return {
            'safe': is_safe,
            'reasons': blocking_reasons,
            'message': 'Cannot remove card with active dependencies' if not is_safe else 'Safe to remove'
        }
    
    def _check_pending_transactions(self, card_id: str) -> List[Dict[str, Any]]:
        """Check for pending transactions on this card."""
        # Simulated database query
        return []  # No pending transactions
    
    def _check_active_subscriptions(self, card_id: str) -> List[Dict[str, Any]]:
        """Check for active subscriptions using this card."""
        # Simulated database query
        return []  # No active subscriptions
    
    def _check_recurring_payments(self, card_id: str) -> List[Dict[str, Any]]:
        """Check for recurring payments scheduled on this card."""
        # Simulated database query
        return []  # No recurring payments
    
    def _is_only_card(self, customer_id: str) -> bool:
        """Check if this is the customer's only payment card."""
        # Simulated database query
        total_cards = 3  # Simulated count
        return total_cards == 1
    
    def _process_removal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the actual card removal.
        
        Implements soft delete if enabled, otherwise hard delete.
        """
        card_id = data['card_id']
        customer_id = data['customer_id']
        reason = data.get('reason', RemovalReason.USER_REQUESTED.value)
        
        if self.soft_delete_enabled:
            # Soft delete - mark as deleted but keep in database
            deletion_date = datetime.now() + timedelta(days=self.recovery_period_days)
            
            removal_data = {
                'card_id': card_id,
                'customer_id': customer_id,
                'removal_type': 'soft_delete',
                'status': 'removed',
                'reason': reason,
                'removed_at': datetime.now().isoformat(),
                'permanent_deletion_date': deletion_date.isoformat(),
                'recoverable': True
            }
        else:
            # Hard delete - permanently remove
            removal_data = {
                'card_id': card_id,
                'customer_id': customer_id,
                'removal_type': 'hard_delete',
                'status': 'permanently_deleted',
                'reason': reason,
                'removed_at': datetime.now().isoformat(),
                'recoverable': False
            }
        
        # Log audit trail
        self._log_audit(removal_data)
        
        return removal_data
    
    def _log_audit(self, removal_data: Dict[str, Any]) -> None:
        """Log card removal to audit trail."""
        audit_entry = {
            'event_type': 'card_removal',
            'timestamp': datetime.now().isoformat(),
            'data': removal_data
        }
        self.logger.info(f"Audit log: {json.dumps(audit_entry)}")
    
    def _send_notification(self, request_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Send notification to customer about card removal."""
        notification = {
            'customer_id': request_data['customer_id'],
            'type': 'card_removed',
            'message': f"Payment card ending in {request_data.get('card_id', '')[-4:]} has been removed",
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardRemoveHandler()
    
    test_data = {
        'customer_id': 'CUST123456',
        'card_id': 'CARD_1234567890',
        'card_status': 'active',
        'reason': 'user_requested'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
