"""
Payment Card Link Module

This module handles link operations for payment cards.
Provides comprehensive link functionality with proper validation,
error handling, and audit logging.

Features:
- Input validation
- Security checks
- Audit trail logging
- Error handling
- Notification support

Integration points:
- Card management system
- Security services
- Notification system
- Audit logging
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class PaymentCardLinkHandler:
    """
    Handler for link operations on payment cards.
    
    This class manages the complete link workflow including:
    - Input validation
    - Security verification
    - Status updates
    - Audit logging
    - Notification sending
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize link handler.
        
        Args:
            config: Configuration dictionary with operation-specific settings
        """
        self.logger = logger
        self.config = config or {}
        self.enable_notifications = self.config.get('enable_notifications', True)
        self.audit_enabled = self.config.get('audit_enabled', True)

        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute link operation.
        
        Process:
        1. Validate input data
        2. Verify permissions
        3. Check prerequisites
        4. Perform link
        5. Log audit trail
        6. Send notifications
        
        Args:
            data: Dictionary containing:
                - card_id: Card identifier
                - customer_id: Customer identifier
                - Additional link-specific fields
                
        Returns:
            Dictionary with operation status and details
        """
        try:
            self.logger.info(f"Processing link for card: {data.get('card_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid link request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify card ownership
            if not self._verify_ownership(data.get('customer_id'), data.get('card_id')):
                return {
                    "status": "error",
                    "message": "Card does not belong to this customer",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check prerequisites
            if not self._check_prerequisites(data):
                return {
                    "status": "error",
                    "message": "Prerequisites not met for link",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process link
            result = self._process_link(data)
            
            # Log audit trail
            if self.audit_enabled:
                self._log_audit(data, result)
            
            # Send notification
            if self.enable_notifications:
                self._send_notification(data, result)
            
            self.logger.info(f"Link completed successfully: {data.get('card_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in link: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to link card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data for link operation."""
        card_id = data.get('card_id')
        customer_id = data.get('customer_id')
        
        if not card_id or not customer_id:
            self.logger.warning("Missing required fields")
            return False
        
        return True
    
    def _verify_ownership(self, customer_id: str, card_id: str) -> bool:
        """Verify card belongs to customer."""
        # Simulated database query
        stored_customer_id = "CUST123456"
        return stored_customer_id == customer_id
    
    def _check_prerequisites(self, data: Dict[str, Any]) -> bool:
        """Check if prerequisites are met for link."""
        # Simulated prerequisite checks
        card_status = self._get_card_status(data.get('card_id'))
        
        # Operation-specific prerequisite logic
        return card_status in ['active', 'inactive', 'blocked']
    
    def _get_card_status(self, card_id: str) -> str:
        """Get current card status."""
        # Simulated database query
        return 'active'
    
    def _process_link(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the link operation.
        
        Performs the actual link logic and updates card status.
        """
        card_id = data['card_id']
        customer_id = data['customer_id']
        
        result_data = {
            'card_id': card_id,
            'customer_id': customer_id,
            'operation': 'link',
            'status': 'linkd',
            'timestamp': datetime.now().isoformat(),
            'processed_by': customer_id
        }
        
        # Simulated database update
        self.logger.info(f"Processing link for card: {card_id}")
        
        return result_data
    
    def _log_audit(self, request_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Log link operation to audit trail."""
        audit_entry = {
            'event_type': 'card_link',
            'customer_id': request_data['customer_id'],
            'card_id': request_data['card_id'],
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        self.logger.info(f"Audit log: {json.dumps(audit_entry)}")
    
    def _send_notification(self, request_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Send notification about link operation."""
        notification = {
            'customer_id': request_data['customer_id'],
            'type': 'card_link',
            'message': f"Card link operation completed for card ending in {request_data['card_id'][-4:]}",
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardLinkHandler()
    
    test_data = {
        'card_id': 'CARD_1234567890',
        'customer_id': 'CUST123456'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
