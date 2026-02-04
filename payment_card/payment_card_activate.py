"""
Payment Card Activation Module

This module handles the activation of newly issued or replacement payment cards.
Card activation is a security measure that ensures the card has been received
by the legitimate cardholder before it can be used for transactions.

Activation process:
- Verify card ownership
- Validate activation code
- Check card status
- Activate card in system
- Enable for transactions
- Send confirmation notification

Security features:
- Multi-factor authentication
- Activation code verification
- Time-limited activation window
- Fraud detection integration
- Suspicious activity monitoring

Business rules:
- Cards must be activated within 60 days of issuance
- Activation requires last 4 digits + activation code
- Failed activation attempts are logged
- Maximum 5 activation attempts allowed
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class CardActivationError(Exception):
    """Custom exception for card activation errors"""
    pass

class PaymentCardActivateHandler:
    """
    Handler for activating payment cards.
    
    Manages the card activation workflow including:
    - Ownership verification
    - Activation code validation
    - Status updates
    - Notification sending
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize card activation handler.
        
        Args:
            config: Configuration dictionary with:
                - max_activation_attempts: Maximum activation attempts
                - activation_window_days: Days allowed for activation
                - require_activation_code: Require activation code
        """
        self.logger = logger
        self.config = config or {}
        self.max_activation_attempts = self.config.get('max_activation_attempts', 5)
        self.activation_window_days = self.config.get('activation_window_days', 60)
        self.require_activation_code = self.config.get('require_activation_code', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute card activation.
        
        Process:
        1. Validate input data
        2. Verify card exists and is inactive
        3. Check activation window
        4. Verify activation code
        5. Check activation attempts
        6. Activate card
        7. Send confirmation
        
        Args:
            data: Dictionary containing:
                - card_id: Card to activate
                - user_id: User requesting activation
                - activation_code: Activation code (optional)
                - last_four_digits: Last 4 digits of card
                
        Returns:
            Dictionary with activation status
        """
        try:
            self.logger.info(f"Processing card activation for card: {data.get('card_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid activation request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check card status
            card_status = self._get_card_status(data.get('card_id'))
            if card_status != 'inactive':
                return {
                    "status": "error",
                    "message": f"Card cannot be activated. Current status: {card_status}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check activation window
            if not self._check_activation_window(data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Activation window has expired. Please request a new card.",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify activation code
            if self.require_activation_code:
                if not self._verify_activation_code(data):
                    return {
                        "status": "error",
                        "message": "Invalid activation code",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Check activation attempts
            if not self._check_activation_attempts(data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Maximum activation attempts exceeded. Card has been locked.",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process activation
            result = self._process_activation(data)
            
            self.logger.info(f"Card activated successfully: {data.get('card_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error activating card: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to activate card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate activation request data.
        
        Checks:
        - Required fields present
        - Valid data types
        - Card ID format
        """
        if not data.get('card_id'):
            self.logger.warning("Missing card_id")
            return False
        
        if not data.get('user_id'):
            self.logger.warning("Missing user_id")
            return False
        
        if self.require_activation_code and not data.get('activation_code'):
            self.logger.warning("Missing activation_code")
            return False
        
        return True
    
    def _get_card_status(self, card_id: str) -> str:
        """Get current card status from database."""
        # Simulated database query
        return 'inactive'
    
    def _check_activation_window(self, card_id: str) -> bool:
        """
        Check if card is within activation window.
        
        Cards must be activated within configured days of issuance.
        """
        # Simulated database query for card issuance date
        issued_date = datetime.now() - timedelta(days=10)
        
        activation_deadline = issued_date + timedelta(days=self.activation_window_days)
        
        return datetime.now() <= activation_deadline
    
    def _verify_activation_code(self, data: Dict[str, Any]) -> bool:
        """
        Verify activation code matches stored code.
        
        Activation codes are typically sent via:
        - SMS to registered phone
        - Email to registered email
        - Physical mail with card
        """
        provided_code = data.get('activation_code')
        
        # Simulated database query for stored activation code
        stored_code = "ABC123"
        
        return provided_code == stored_code
    
    def _check_activation_attempts(self, card_id: str) -> bool:
        """
        Check if activation attempts are within limit.
        
        Tracks failed activation attempts to prevent brute force.
        """
        # Simulated database query for attempt count
        attempt_count = 2
        
        return attempt_count < self.max_activation_attempts
    
    def _process_activation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the card activation.
        
        Steps:
        1. Update card status to active
        2. Record activation timestamp
        3. Link to user account
        4. Enable for transactions
        5. Send confirmation notification
        """
        card_id = data['card_id']
        user = data.get('user', {})
        
        # BUG: Should use 'customer_id' field not 'id'
        customer_id = user.get('id')
        
        activation_data = {
            'card_id': card_id,
            'customer_id': customer_id,
            'status': 'activated',
            'activated_at': datetime.now().isoformat(),
            'activated_by': data.get('user_id'),
            'activation_method': 'online'
        }
        
        # Simulated database update
        self.logger.info(f"Activating card: {card_id}")
        
        # Send confirmation notification
        self._send_activation_confirmation(activation_data)
        
        return activation_data
    
    def _send_activation_confirmation(self, activation_data: Dict[str, Any]) -> None:
        """Send activation confirmation to customer."""
        notification = {
            'customer_id': activation_data['customer_id'],
            'type': 'card_activated',
            'message': f"Your card ending in {activation_data['card_id'][-4:]} has been activated",
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending activation confirmation: {notification}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardActivateHandler()
    
    test_data = {
        'card_id': 'CARD_1234567890',
        'user_id': 'USER_123',
        'user': {
            'id': 'USR_789',  # Wrong field - should be customer_id
            'customer_id': 'CUST_123'
        },
        'activation_code': 'ABC123',
        'last_four_digits': '7890'
    }
    
    result = handler.execute(test_data)
    print(result)
