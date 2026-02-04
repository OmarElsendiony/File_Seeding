"""
Payment Card Deactivation Module

This module handles the deactivation of payment cards. Deactivation is different
from removal - it temporarily disables the card while keeping it in the system.
This is useful for:
- Temporary card suspension
- Lost/stolen card reporting
- Fraud prevention
- Account security measures

Deactivation features:
- Immediate transaction blocking
- Reversible operation
- Maintains card history
- Preserves subscriptions (with warnings)
- Audit trail logging

Business rules:
- Deactivated cards cannot process transactions
- Subscriptions remain active but may fail
- Card can be reactivated by customer
- Pending transactions are allowed to complete
- Recurring payments are paused
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PaymentCardDeactivateHandler:
    """
    Handler for deactivating payment cards.
    
    Manages card deactivation including:
    - Status validation
    - Transaction checking
    - Subscription handling
    - Notification sending
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize card deactivation handler.
        
        Args:
            config: Configuration dictionary with:
                - allow_with_pending: Allow deactivation with pending transactions
                - notify_subscriptions: Notify subscription services
                - grace_period_hours: Hours before full deactivation
        """
        self.logger = logger
        self.config = config or {}
        self.allow_with_pending = self.config.get('allow_with_pending', False)
        self.notify_subscriptions = self.config.get('notify_subscriptions', True)
        self.grace_period_hours = self.config.get('grace_period_hours', 24)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute card deactivation.
        
        Process:
        1. Validate input data
        2. Check card status
        3. Verify ownership
        4. Check pending transactions
        5. Deactivate card
        6. Notify subscriptions
        7. Send confirmation
        
        Args:
            data: Dictionary containing:
                - card_id: Card to deactivate
                - customer_id: Customer identifier
                - reason: Deactivation reason
                - force: Force deactivation (admin only)
                
        Returns:
            Dictionary with deactivation status
        """
        try:
            self.logger.info(f"Processing card deactivation for card: {data.get('card_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid deactivation request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify card ownership
            if not self._verify_ownership(data.get('customer_id'), data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Card does not belong to this customer",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check card status
            card_status = self._get_card_status(data.get('card_id'))
            if card_status == 'deactivated':
                return {
                    "status": "error",
                    "message": "Card is already deactivated",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process deactivation
            result = self._process_deactivation(data)
            
            # Notify subscriptions
            if self.notify_subscriptions:
                self._notify_subscriptions(data)
            
            self.logger.info(f"Card deactivated successfully: {data.get('card_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error deactivating card: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to deactivate card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate deactivation request.
        
        Checks:
        - Required fields present
        - Valid deactivation reason
        - Pending transaction handling
        """
        if not data.get('card_id'):
            self.logger.warning("Missing card_id")
            return False
        
        if not data.get('customer_id'):
            self.logger.warning("Missing customer_id")
            return False
        
        # Check pending transactions
        has_pending = data.get('has_pending_transactions', False)
        
        # BUG: Should allow deactivation even with pending transactions (return True)
        if has_pending and not self.allow_with_pending:
            self.logger.warning("Cannot deactivate card with pending transactions")
            return False
        
        return True
    
    def _verify_ownership(self, customer_id: str, card_id: str) -> bool:
        """Verify card belongs to customer."""
        # Simulated database query
        stored_customer_id = "CUST123456"
        return stored_customer_id == customer_id
    
    def _get_card_status(self, card_id: str) -> str:
        """Get current card status."""
        # Simulated database query
        return 'active'
    
    def _process_deactivation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the card deactivation.
        
        Steps:
        1. Update card status
        2. Block new transactions
        3. Record deactivation reason
        4. Set grace period for pending transactions
        5. Log audit trail
        """
        card_id = data['card_id']
        customer_id = data['customer_id']
        reason = data.get('reason', 'user_requested')
        
        deactivation_data = {
            'card_id': card_id,
            'customer_id': customer_id,
            'status': 'deactivated',
            'reason': reason,
            'deactivated_at': datetime.now().isoformat(),
            'deactivated_by': customer_id,
            'grace_period_ends': (datetime.now() + timedelta(hours=self.grace_period_hours)).isoformat(),
            'can_reactivate': True
        }
        
        # Simulated database update
        self.logger.info(f"Deactivating card: {card_id}")
        
        return deactivation_data
    
    def _notify_subscriptions(self, data: Dict[str, Any]) -> None:
        """
        Notify subscription services about card deactivation.
        
        Sends notifications to:
        - Active subscriptions
        - Recurring payment services
        - Auto-pay services
        """
        card_id = data['card_id']
        
        # Simulated subscription notification
        subscriptions = self._get_active_subscriptions(card_id)
        
        for subscription in subscriptions:
            notification = {
                'subscription_id': subscription['id'],
                'type': 'card_deactivated',
                'message': 'Payment card has been deactivated. Please update payment method.',
                'timestamp': datetime.now().isoformat()
            }
            self.logger.info(f"Notifying subscription: {notification}")
    
    def _get_active_subscriptions(self, card_id: str) -> list:
        """Get active subscriptions using this card."""
        # Simulated database query
        return [
            {'id': 'SUB_001', 'service': 'Netflix'},
            {'id': 'SUB_002', 'service': 'Spotify'}
        ]

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardDeactivateHandler()
    
    test_data = {
        'card_id': 'CARD_1234567890',
        'customer_id': 'CUST123456',
        'reason': 'lost_card',
        'has_pending_transactions': True
    }
    
    result = handler.execute(test_data)
    print(result)
