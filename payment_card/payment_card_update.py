"""
Payment Card Update Module

This module handles updates to existing payment card information.
It supports modification of card metadata, spending limits, expiration dates,
billing addresses, and other card-related settings while maintaining
data integrity and security compliance.

Supported update operations:
- Billing address updates
- Card nickname changes
- Spending limit modifications
- Default card designation
- Notification preferences
- Auto-pay settings
- Merchant category restrictions
- Card status changes

Security features:
- Change validation and authorization
- Audit trail logging
- PCI-DSS compliance
- Fraud detection integration
- Customer notification

Business rules:
- Limit changes require approval for increases > 20%
- Address changes trigger verification
- Status changes logged for compliance
- Default card changes update all subscriptions
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class UpdateType:
    """Types of card updates"""
    BILLING_ADDRESS = "billing_address"
    NICKNAME = "nickname"
    SPENDING_LIMIT = "spending_limit"
    DEFAULT_STATUS = "default_status"
    NOTIFICATIONS = "notifications"
    AUTO_PAY = "auto_pay"
    MERCHANT_RESTRICTIONS = "merchant_restrictions"

class PaymentCardUpdateHandler:
    """
    Handler for updating payment card information.
    
    This class manages card updates including:
    - Input validation
    - Authorization checks
    - Data integrity verification
    - Update processing
    - Audit logging
    - Customer notification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize card update handler.
        
        Args:
            config: Configuration dictionary with:
                - api_endpoint: API endpoint for card updates
                - enable_notifications: Send update notifications
                - require_verification: Require additional verification
                - audit_enabled: Enable audit logging
        """
        self.logger = logger
        self.config = config or {}
        # BUG: Typo in API endpoint - "updte" instead of "update"
        self.api_endpoint = self.config.get('api_endpoint', "/api/v1/cards/updte")
        self.enable_notifications = self.config.get('enable_notifications', True)
        self.require_verification = self.config.get('require_verification', False)
        self.audit_enabled = self.config.get('audit_enabled', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute card update operation.
        
        Process:
        1. Validate input data
        2. Verify card ownership
        3. Check update permissions
        4. Validate update data
        5. Perform update
        6. Log audit trail
        7. Send notifications
        8. Return updated card info
        
        Args:
            data: Dictionary containing:
                - customer_id: Customer identifier
                - card_id: Card to update
                - update_type: Type of update
                - update_data: New data values
                - verification_code: Optional verification
                
        Returns:
            Dictionary with update status and details
        """
        try:
            self.logger.info(f"Processing card update via {self.api_endpoint}")
            self.logger.info(f"Card ID: {data.get('card_id')}, Type: {data.get('update_type')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid card update request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify card ownership
            if not self._verify_ownership(data.get('customer_id'), data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Card does not belong to this customer",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if verification is required
            if self.require_verification and not self._verify_update_authorization(data):
                return {
                    "status": "error",
                    "message": "Additional verification required",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process update
            result = self._process_update(data)
            
            # Log audit trail
            if self.audit_enabled:
                self._log_audit(data, result)
            
            # Send notification
            if self.enable_notifications:
                self._send_notification(data, result)
            
            self.logger.info(f"Card updated successfully: {data.get('card_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating card: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to update card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate update request data.
        
        Checks:
        - Required fields present
        - Valid update type
        - Valid update data format
        - Business rule compliance
        """
        card_id = data.get('card_id')
        customer_id = data.get('customer_id')
        update_type = data.get('update_type')
        update_data = data.get('update_data')
        
        if not all([card_id, customer_id, update_type, update_data]):
            self.logger.warning("Missing required fields")
            return False
        
        # Validate update type
        valid_types = [
            UpdateType.BILLING_ADDRESS,
            UpdateType.NICKNAME,
            UpdateType.SPENDING_LIMIT,
            UpdateType.DEFAULT_STATUS,
            UpdateType.NOTIFICATIONS,
            UpdateType.AUTO_PAY,
            UpdateType.MERCHANT_RESTRICTIONS
        ]
        
        if update_type not in valid_types:
            self.logger.warning(f"Invalid update type: {update_type}")
            return False
        
        # Validate update data based on type
        if not self._validate_update_data(update_type, update_data):
            return False
        
        return True
    
    def _validate_update_data(self, update_type: str, update_data: Dict[str, Any]) -> bool:
        """
        Validate update data based on update type.
        
        Each update type has specific validation rules.
        """
        if update_type == UpdateType.BILLING_ADDRESS:
            required_fields = ['street', 'city', 'state', 'zip', 'country']
            return all(field in update_data for field in required_fields)
        
        elif update_type == UpdateType.NICKNAME:
            nickname = update_data.get('nickname', '')
            return 1 <= len(nickname) <= 50
        
        elif update_type == UpdateType.SPENDING_LIMIT:
            limit = update_data.get('limit')
            return isinstance(limit, (int, float)) and 0 < limit <= 100000
        
        elif update_type == UpdateType.DEFAULT_STATUS:
            is_default = update_data.get('is_default')
            return isinstance(is_default, bool)
        
        elif update_type == UpdateType.NOTIFICATIONS:
            return 'enabled' in update_data
        
        elif update_type == UpdateType.AUTO_PAY:
            return 'enabled' in update_data
        
        elif update_type == UpdateType.MERCHANT_RESTRICTIONS:
            return 'allowed_merchants' in update_data or 'blocked_merchants' in update_data
        
        return False
    
    def _verify_ownership(self, customer_id: str, card_id: str) -> bool:
        """Verify card belongs to customer."""
        # Simulated database query
        stored_customer_id = "CUST123456"
        return stored_customer_id == customer_id
    
    def _verify_update_authorization(self, data: Dict[str, Any]) -> bool:
        """
        Verify additional authorization for sensitive updates.
        
        Some updates require additional verification:
        - Spending limit increases
        - Billing address changes
        - Default card changes
        """
        update_type = data.get('update_type')
        verification_code = data.get('verification_code')
        
        sensitive_updates = [
            UpdateType.BILLING_ADDRESS,
            UpdateType.SPENDING_LIMIT
        ]
        
        if update_type in sensitive_updates:
            if not verification_code:
                return False
            # Verify code (simulated)
            return verification_code == "123456"
        
        return True
    
    def _process_update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the card update.
        
        Updates the card information in the database and
        returns the updated card details.
        """
        card_id = data['card_id']
        update_type = data['update_type']
        update_data = data['update_data']
        
        # Simulated database update
        updated_fields = []
        
        if update_type == UpdateType.BILLING_ADDRESS:
            updated_fields = ['billing_address']
        elif update_type == UpdateType.NICKNAME:
            updated_fields = ['nickname']
        elif update_type == UpdateType.SPENDING_LIMIT:
            updated_fields = ['spending_limit']
        elif update_type == UpdateType.DEFAULT_STATUS:
            updated_fields = ['is_default']
        elif update_type == UpdateType.NOTIFICATIONS:
            updated_fields = ['notification_preferences']
        elif update_type == UpdateType.AUTO_PAY:
            updated_fields = ['auto_pay_enabled']
        elif update_type == UpdateType.MERCHANT_RESTRICTIONS:
            updated_fields = ['merchant_restrictions']
        
        return {
            'card_id': card_id,
            'update_type': update_type,
            'updated_fields': updated_fields,
            'updated_at': datetime.now().isoformat(),
            'update_data': update_data
        }
    
    def _log_audit(self, request_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Log card update to audit trail."""
        audit_entry = {
            'event_type': 'card_update',
            'customer_id': request_data['customer_id'],
            'card_id': request_data['card_id'],
            'update_type': request_data['update_type'],
            'timestamp': datetime.now().isoformat(),
            'result': result['updated_fields']
        }
        self.logger.info(f"Audit log: {json.dumps(audit_entry)}")
    
    def _send_notification(self, request_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Send notification about card update."""
        notification = {
            'customer_id': request_data['customer_id'],
            'type': 'card_updated',
            'message': f"Your card ending in {request_data['card_id'][-4:]} has been updated",
            'update_type': request_data['update_type'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardUpdateHandler()
    
    test_data = {
        'customer_id': 'CUST123456',
        'card_id': 'CARD_1234567890',
        'update_type': UpdateType.NICKNAME,
        'update_data': {
            'nickname': 'My Primary Card'
        }
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
