"""
Payment Transfer Cancellation Module

This module handles the cancellation of pending payment transfers.
Transfers can only be cancelled if they haven't been processed yet.

Cancellation features:
- Status validation
- Timing checks
- Fund release
- Notification sending
- Audit logging

Business rules:
- Only pending/scheduled transfers can be cancelled
- Processing transfers cannot be cancelled
- Completed transfers require reversal, not cancellation
- Cancelled transfers release reserved funds immediately
- Cancellation fees may apply for certain transfer types
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class PaymentTransferCancelHandler:
    """
    Handler for cancelling payment transfers.
    
    Manages transfer cancellation including:
    - Status validation
    - Cancellation eligibility
    - Fund release
    - Notification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transfer cancellation handler.
        
        Args:
            config: Configuration dictionary with:
                - allow_processing_cancel: Allow cancellation of processing transfers
                - cancellation_fee: Fee for cancelling transfers
                - notification_enabled: Send cancellation notifications
        """
        self.logger = logger
        self.config = config or {}
        self.allow_processing_cancel = self.config.get('allow_processing_cancel', False)
        self.cancellation_fee = self.config.get('cancellation_fee', 0.00)
        self.notification_enabled = self.config.get('notification_enabled', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute transfer cancellation.
        
        Process:
        1. Validate input
        2. Verify transfer exists
        3. Check transfer status
        4. Verify ownership
        5. Cancel transfer
        6. Release funds
        7. Send notification
        
        Args:
            data: Dictionary containing:
                - transfer_id: Transfer to cancel
                - customer_id: Customer requesting cancellation
                - reason: Cancellation reason
                
        Returns:
            Dictionary with cancellation status
        """
        try:
            self.logger.info(f"Processing transfer cancellation: {data.get('transfer_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid cancellation request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get transfer details
            transfer = self._get_transfer(data.get('transfer_id'))
            if not transfer:
                return {
                    "status": "error",
                    "message": "Transfer not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if cancellable
            if not self._is_cancellable(transfer):
                return {
                    "status": "error",
                    "message": f"Transfer cannot be cancelled. Current status: {transfer['status']}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify ownership
            if not self._verify_ownership(data.get('customer_id'), transfer):
                return {
                    "status": "error",
                    "message": "Unauthorized cancellation request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process cancellation
            result = self._process_cancellation(data, transfer)
            
            self.logger.info(f"Transfer cancelled successfully: {data.get('transfer_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error cancelling transfer: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to cancel transfer: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate cancellation request."""
        if not data.get('transfer_id'):
            self.logger.warning("Missing transfer_id")
            return False
        
        if not data.get('customer_id'):
            self.logger.warning("Missing customer_id")
            return False
        
        return True
    
    def _get_transfer(self, transfer_id: str) -> Optional[Dict[str, Any]]:
        """Get transfer details from database."""
        # Simulated database query
        return {
            'transfer_id': transfer_id,
            'source_account_id': 'ACC_123456',
            'destination_account_id': 'ACC_789012',
            'amount': '500.00',
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
    
    def _is_cancellable(self, transfer: Dict[str, Any]) -> bool:
        """
        Check if transfer can be cancelled.
        
        Cancellable statuses:
        - pending
        - scheduled
        - initiated (if allow_processing_cancel is True)
        """
        status = transfer.get('status')
        
        # BUG: Status comparison should use lowercase
        if status == "PENDING":
            return True
        
        if status in ['scheduled', 'initiated']:
            return True
        
        if status == 'processing' and self.allow_processing_cancel:
            return True
        
        return False
    
    def _verify_ownership(self, customer_id: str, transfer: Dict[str, Any]) -> bool:
        """Verify customer owns the source account."""
        # Simulated verification
        source_account_owner = "CUST123456"
        return True  # Simplified for example
    
    def _process_cancellation(self, data: Dict[str, Any], transfer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the transfer cancellation.
        
        Steps:
        1. Update transfer status
        2. Release reserved funds
        3. Apply cancellation fee (if any)
        4. Log cancellation
        5. Send notification
        """
        transfer_id = data['transfer_id']
        
        cancellation_data = {
            'transfer_id': transfer_id,
            'original_status': transfer['status'],
            'new_status': 'cancelled',
            'cancelled_at': datetime.now().isoformat(),
            'cancelled_by': data.get('customer_id'),
            'cancellation_reason': data.get('reason', 'user_requested'),
            'cancellation_fee': self.cancellation_fee,
            'funds_released': True
        }
        
        # Simulated database update
        self.logger.info(f"Cancelling transfer: {transfer_id}")
        
        # Send notification
        if self.notification_enabled:
            self._send_notification(cancellation_data)
        
        return cancellation_data
    
    def _send_notification(self, cancellation_data: Dict[str, Any]) -> None:
        """Send cancellation notification."""
        notification = {
            'type': 'transfer_cancelled',
            'transfer_id': cancellation_data['transfer_id'],
            'message': 'Your transfer has been cancelled',
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    handler = PaymentTransferCancelHandler()
    
    test_data = {
        'transfer_id': 'TXF_123456',
        'customer_id': 'CUST123456',
        'reason': 'Changed my mind'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
