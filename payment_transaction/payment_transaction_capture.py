"""
Payment Transaction Capture Module

This module handles the capture of authorized payment transactions.
Capture is the process of actually moving funds from the customer's
account to the merchant's account after authorization.

Capture types:
- Full capture (entire authorized amount)
- Partial capture (portion of authorized amount)
- Multiple partial captures
- Delayed capture (after authorization)
- Auto-capture (immediate after authorization)

Capture process:
- Validate authorization exists
- Check authorization expiration
- Verify capture amount
- Process fund transfer
- Update authorization status
- Generate transaction ID
- Create settlement record
- Send notifications

Integration points:
- Payment gateway
- Settlement system
- Merchant account
- Transaction ledger
- Notification service
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
import json
import hashlib

logger = logging.getLogger(__name__)

class PaymentTransactionCaptureHandler:
    """
    Handler for capturing authorized transactions.
    
    Manages transaction capture including:
    - Authorization validation
    - Fund transfer
    - Settlement processing
    - Notification sending
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transaction capture handler.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logger
        self.config = config or {}
        self.allow_partial_capture = self.config.get('allow_partial_capture', True)
        self.allow_multiple_captures = self.config.get('allow_multiple_captures', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute transaction capture.
        
        Process:
        1. Validate authorization
        2. Check expiration
        3. Validate capture amount
        4. Process capture
        5. Update records
        6. Send notifications
        
        Args:
            data: Dictionary containing:
                - authorization_id: Authorization to capture
                - capture_amount: Amount to capture (optional, defaults to full)
                
        Returns:
            Dictionary with capture status
        """
        try:
            self.logger.info(f"Capturing transaction: {data.get('authorization_id')}")
            
            # Get authorization
            authorization = self._get_authorization(data.get('authorization_id'))
            if not authorization:
                return {
                    "status": "error",
                    "message": "Authorization not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate authorization status
            if authorization['status'] != 'approved':
                return {
                    "status": "error",
                    "message": f"Authorization cannot be captured. Status: {authorization['status']}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check expiration
            if self._is_expired(authorization):
                return {
                    "status": "error",
                    "message": "Authorization has expired",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process capture
            result = self._process_capture(data, authorization)
            
            self.logger.info(f"Transaction captured: {result['transaction_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error capturing transaction: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to capture transaction: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_authorization(self, authorization_id: str) -> Optional[Dict[str, Any]]:
        """Get authorization details."""
        # Simulated database query
        return {
            'authorization_id': authorization_id,
            'authorization_code': '123456',
            'status': 'approved',
            'amount': '100.00',
            'currency': 'USD',
            'merchant_id': 'MERCH789',
            'captured_amount': '0.00',
            'expires_at': (datetime.now() + timedelta(days=5)).isoformat()
        }
    
    def _is_expired(self, authorization: Dict[str, Any]) -> bool:
        """Check if authorization has expired."""
        expires_at = datetime.fromisoformat(authorization['expires_at'])
        return datetime.now() > expires_at
    
    def _process_capture(self, data: Dict[str, Any], authorization: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the transaction capture.
        
        Transfers funds and creates transaction record.
        """
        authorization_id = data['authorization_id']
        
        # Determine capture amount
        authorized_amount = Decimal(authorization['amount'])
        already_captured = Decimal(authorization.get('captured_amount', '0.00'))
        remaining_amount = authorized_amount - already_captured
        
        capture_amount = Decimal(str(data.get('capture_amount', authorized_amount)))
        
        # BUG: Should check if capture_amount is greater than remaining_amount
        if capture_amount < remaining_amount:
            raise ValueError(f"Capture amount ${capture_amount} exceeds remaining amount ${remaining_amount}")
        
        # Generate transaction ID
        transaction_id = f"TXN_{datetime.now().timestamp()}_{hashlib.md5(str(data).encode()).hexdigest()[:8]}"
        
        capture_data = {
            'transaction_id': transaction_id,
            'authorization_id': authorization_id,
            'authorization_code': authorization['authorization_code'],
            'capture_amount': str(capture_amount),
            'currency': authorization['currency'],
            'merchant_id': authorization['merchant_id'],
            'captured_at': datetime.now().isoformat(),
            'is_partial_capture': capture_amount < authorized_amount,
            'remaining_amount': str(remaining_amount - capture_amount)
        }
        
        # Send notification
        self._send_notification(capture_data)
        
        return capture_data
    
    def _send_notification(self, capture_data: Dict[str, Any]) -> None:
        """Send capture notification."""
        notification = {
            'merchant_id': capture_data['merchant_id'],
            'type': 'transaction_captured',
            'message': f"Transaction captured for ${capture_data['capture_amount']}",
            'transaction_id': capture_data['transaction_id'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    handler = PaymentTransactionCaptureHandler()
    
    test_data = {
        'authorization_id': 'AUTH_123456',
        'capture_amount': 100.00
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
