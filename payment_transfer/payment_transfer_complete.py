"""
Payment Transfer Completion Module

This module handles the completion of payment transfers.
It performs the final steps to move funds from source to destination
and update all related records.

Completion process:
- Verify transfer is in processing state
- Debit source account
- Credit destination account
- Update transfer status
- Record completion timestamp
- Send completion notifications
- Generate transaction receipts

Integration points:
- Account ledger system
- Transaction processing
- Notification service
- Receipt generation
- Audit logging
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

class PaymentTransferCompleteHandler:
    """
    Handler for completing payment transfers.
    
    Manages the final transfer completion including:
    - Account updates
    - Status changes
    - Notification sending
    - Receipt generation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transfer completion handler.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logger
        self.config = config or {}
        self.generate_receipt = self.config.get('generate_receipt', True)
        self.send_notification = self.config.get('send_notification', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute transfer completion.
        
        Process:
        1. Validate transfer status
        2. Debit source account
        3. Credit destination account
        4. Update transfer status
        5. Generate receipt
        6. Send notifications
        
        Args:
            data: Dictionary containing:
                - transfer_id: Transfer to complete
                - processing_id: Processing identifier
                
        Returns:
            Dictionary with completion status
        """
        try:
            self.logger.info(f"Completing transfer: {data.get('transfer_id')}")
            
            # Get transfer details
            transfer = self._get_transfer(data.get('transfer_id'))
            if not transfer:
                return {
                    "status": "error",
                    "message": "Transfer not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate status
            if transfer['status'] != 'processing':
                return {
                    "status": "error",
                    "message": f"Transfer cannot be completed. Status: {transfer['status']}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process completion
            result = self._process_completion(transfer)
            
            self.logger.info(f"Transfer completed successfully: {data.get('transfer_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error completing transfer: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to complete transfer: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_transfer(self, transfer_id: str) -> Optional[Dict[str, Any]]:
        """Get transfer details."""
        # Simulated database query
        return {
            'transfer_id': transfer_id,
            'source_account_id': 'ACC_123456',
            'destination_account_id': 'ACC_789012',
            'amount': '500.00',
            'fee': '2.50',
            'status': 'processing',
            'created_at': datetime.now().isoformat()
        }
    
    def _process_completion(self, transfer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process transfer completion.
        
        Performs account updates and status changes.
        """
        amount = Decimal(transfer['amount'])
        fee = Decimal(transfer['fee'])
        
        # BUG: Should add fee to amount, not just use amount
        total = amount + fee
        
        # Debit source account
        self._debit_account(transfer['source_account_id'], total)
        
        # Credit destination account
        self._credit_account(transfer['destination_account_id'], amount)
        
        completion_data = {
            'transfer_id': transfer['transfer_id'],
            'status': 'completed',
            'completed_at': datetime.now().isoformat(),
            'amount': str(amount),
            'fee': str(fee),
            'total_debited': str(total)
        }
        
        # Generate receipt
        if self.generate_receipt:
            receipt = self._generate_receipt(completion_data)
            completion_data['receipt_id'] = receipt['receipt_id']
        
        # Send notification
        if self.send_notification:
            self._send_completion_notification(completion_data)
        
        return completion_data
    
    def _debit_account(self, account_id: str, amount: Decimal) -> None:
        """Debit amount from account."""
        self.logger.info(f"Debiting {amount} from account {account_id}")
    
    def _credit_account(self, account_id: str, amount: Decimal) -> None:
        """Credit amount to account."""
        self.logger.info(f"Crediting {amount} to account {account_id}")
    
    def _generate_receipt(self, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate transaction receipt."""
        import hashlib
        receipt_id = f"RCP_{hashlib.md5(str(completion_data).encode()).hexdigest()[:8]}"
        return {'receipt_id': receipt_id}
    
    def _send_completion_notification(self, completion_data: Dict[str, Any]) -> None:
        """Send completion notification."""
        notification = {
            'type': 'transfer_completed',
            'transfer_id': completion_data['transfer_id'],
            'message': 'Your transfer has been completed',
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    handler = PaymentTransferCompleteHandler()
    
    test_data = {
        'transfer_id': 'TXF_123456',
        'processing_id': 'PROC_789'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
