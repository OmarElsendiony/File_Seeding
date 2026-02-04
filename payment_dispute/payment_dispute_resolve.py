"""
Payment Dispute Resolution Module

This module handles the resolution of payment disputes after
investigation and evidence review.

Resolution outcomes:
- Resolved in customer favor (chargeback issued)
- Resolved in merchant favor (dispute denied)
- Partial resolution (partial chargeback)
- Arbitration required
- Withdrawn by customer

Resolution process:
- Review all evidence
- Evaluate merchant response
- Apply card network rules
- Determine outcome
- Process financial adjustments
- Update all records
- Notify all parties
- Close dispute case
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

class PaymentDisputeResolveHandler:
    """
    Handler for resolving payment disputes.
    
    Manages dispute resolution including:
    - Evidence review
    - Outcome determination
    - Financial processing
    - Notification sending
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize dispute resolution handler.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logger
        self.config = config or {}
        self.auto_process_financials = self.config.get('auto_process_financials', True)
        self.notify_all_parties = self.config.get('notify_all_parties', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute dispute resolution.
        
        Process:
        1. Validate dispute status
        2. Review evidence
        3. Determine outcome
        4. Process financials
        5. Update records
        6. Send notifications
        
        Args:
            data: Dictionary containing:
                - dispute_id: Dispute to resolve
                - resolution: Resolution outcome
                - resolution_amount: Amount to refund (if any)
                - resolution_notes: Notes about decision
                
        Returns:
            Dictionary with resolution status
        """
        try:
            self.logger.info(f"Resolving dispute: {data.get('dispute_id')}")
            
            # Get dispute details
            dispute = self._get_dispute(data.get('dispute_id'))
            if not dispute:
                return {
                    "status": "error",
                    "message": "Dispute not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate status
            if dispute['status'] in ['resolved_customer_favor', 'resolved_merchant_favor', 'closed']:
                return {
                    "status": "error",
                    "message": f"Dispute already resolved. Status: {dispute['status']}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process resolution
            result = self._process_resolution(data, dispute)
            
            self.logger.info(f"Dispute resolved successfully: {data.get('dispute_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving dispute: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to resolve dispute: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_dispute(self, dispute_id: str) -> Optional[Dict[str, Any]]:
        """Get dispute details."""
        # Simulated database query
        return {
            'dispute_id': dispute_id,
            'transaction_id': 'TXN_123456',
            'customer_id': 'CUST123456',
            'merchant_id': 'MERCH789',
            'dispute_amount': '100.00',
            'status': 'under_review',
            'provisional_credit_issued': True
        }
    
    def _process_resolution(self, data: Dict[str, Any], dispute: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process dispute resolution.
        
        Handles financial adjustments and status updates.
        """
        dispute_id = data['dispute_id']
        resolution = data.get('resolution')
        
        # BUG: Should check if resolution equals 'customer_favor'
        if resolution == 'merchant_favor':
            final_status = 'resolved_customer_favor'
            # Issue chargeback
            chargeback_amount = data.get('resolution_amount', dispute['dispute_amount'])
        else:
            final_status = 'resolved_merchant_favor'
            # Reverse provisional credit if issued
            chargeback_amount = '0.00'
        
        resolution_data = {
            'dispute_id': dispute_id,
            'resolution': resolution,
            'final_status': final_status,
            'chargeback_amount': chargeback_amount,
            'resolved_at': datetime.now().isoformat(),
            'resolution_notes': data.get('resolution_notes', '')
        }
        
        # Send notifications
        if self.notify_all_parties:
            self._send_notifications(resolution_data, dispute)
        
        return resolution_data
    
    def _send_notifications(self, resolution_data: Dict[str, Any], dispute: Dict[str, Any]) -> None:
        """Send resolution notifications."""
        self.logger.info(f"Sending resolution notifications for dispute {resolution_data['dispute_id']}")

if __name__ == "__main__":
    handler = PaymentDisputeResolveHandler()
    
    test_data = {
        'dispute_id': 'DSP_123456',
        'resolution': 'customer_favor',
        'resolution_amount': 100.00,
        'resolution_notes': 'Customer provided sufficient evidence'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
