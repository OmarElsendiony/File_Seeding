"""
Payment Account Closure Module

This module handles the closure of payment accounts.
Account closure is a sensitive operation that requires:
- Balance verification (must be zero or positive)
- Pending transaction checks
- Subscription cancellation
- Final statement generation
- Regulatory compliance

Closure process:
- Verify account ownership
- Check account status
- Validate zero balance
- Cancel subscriptions
- Process final transactions
- Generate closure documents
- Archive account data
- Send confirmation

Business rules:
- Accounts with negative balance cannot be closed
- All pending transactions must be settled
- Subscriptions must be cancelled first
- Final statement is generated
- Account data is archived for 7 years
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class PaymentAccountCloseHandler:
    """
    Handler for closing payment accounts.
    
    Manages account closure including:
    - Balance verification
    - Subscription handling
    - Document generation
    - Data archival
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize account closure handler.
        
        Args:
            config: Configuration dictionary with:
                - allow_negative_closure: Allow closure with negative balance
                - archive_retention_years: Years to retain archived data
                - generate_final_statement: Generate final statement
        """
        self.logger = logger
        self.config = config or {}
        self.allow_negative_closure = self.config.get('allow_negative_closure', False)
        self.archive_retention_years = self.config.get('archive_retention_years', 7)
        self.generate_final_statement = self.config.get('generate_final_statement', True)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute account closure.
        
        Process:
        1. Validate input
        2. Verify ownership
        3. Check account status
        4. Verify balance
        5. Check pending transactions
        6. Cancel subscriptions
        7. Close account
        8. Archive data
        9. Send confirmation
        
        Args:
            data: Dictionary containing:
                - account_id: Account to close
                - customer_id: Customer identifier
                - closure_reason: Reason for closure
                
        Returns:
            Dictionary with closure status
        """
        try:
            self.logger.info(f"Processing account closure: {data.get('account_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid closure request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get account details
            account = self._get_account(data.get('account_id'))
            if not account:
                return {
                    "status": "error",
                    "message": "Account not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify ownership
            if not self._verify_ownership(data.get('customer_id'), account):
                return {
                    "status": "error",
                    "message": "Unauthorized closure request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if closeable
            closeable_check = self._check_closeable(account)
            if not closeable_check['closeable']:
                return {
                    "status": "error",
                    "message": closeable_check['message'],
                    "details": closeable_check['details'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process closure
            result = self._process_closure(data, account)
            
            self.logger.info(f"Account closed successfully: {data.get('account_id')}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error closing account: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to close account: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate closure request."""
        if not data.get('account_id'):
            self.logger.warning("Missing account_id")
            return False
        
        if not data.get('customer_id'):
            self.logger.warning("Missing customer_id")
            return False
        
        return True
    
    def _get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account details."""
        # Simulated database query
        return {
            'account_id': account_id,
            'customer_id': 'CUST123456',
            'account_number': '1234-5678-9012',
            'balance': 0.00,
            'status': 'active',
            'account_type': 'checking'
        }
    
    def _verify_ownership(self, customer_id: str, account: Dict[str, Any]) -> bool:
        """Verify customer owns the account."""
        return account['customer_id'] == customer_id
    
    def _check_closeable(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if account can be closed.
        
        Checks:
        - Account status
        - Balance (must be zero or positive)
        - Pending transactions
        - Active subscriptions
        """
        details = []
        
        # Check status
        if account['status'] == 'closed':
            return {
                'closeable': False,
                'message': 'Account is already closed',
                'details': details
            }
        
        # Check balance
        balance = float(account.get('balance', 0))
        if balance < 0 and not self.allow_negative_closure:
            details.append({
                'type': 'negative_balance',
                'balance': balance,
                'message': 'Account has negative balance'
            })
        
        # Check pending transactions
        pending_txns = self._get_pending_transactions(account['account_id'])
        if pending_txns:
            details.append({
                'type': 'pending_transactions',
                'count': len(pending_txns),
                'message': f'{len(pending_txns)} pending transaction(s)'
            })
        
        # Check subscriptions
        subscriptions = self._get_active_subscriptions(account['account_id'])
        if subscriptions:
            details.append({
                'type': 'active_subscriptions',
                'count': len(subscriptions),
                'message': f'{len(subscriptions)} active subscription(s)'
            })
        
        closeable = len(details) == 0
        
        return {
            'closeable': closeable,
            'message': 'Account cannot be closed' if not closeable else 'Account can be closed',
            'details': details
        }
    
    def _get_pending_transactions(self, account_id: str) -> list:
        """Get pending transactions for account."""
        # Simulated database query
        return []
    
    def _get_active_subscriptions(self, account_id: str) -> list:
        """Get active subscriptions linked to account."""
        # Simulated database query
        return []
    
    def _process_closure(self, data: Dict[str, Any], account: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process account closure.
        
        Steps:
        1. Update account status
        2. Generate final statement
        3. Archive account data
        4. Send confirmation
        """
        account_id = data['account_id']
        
        # Generate final statement
        final_statement = None
        if self.generate_final_statement:
            final_statement = self._generate_final_statement(account)
        
        # Archive data
        archive_id = self._archive_account_data(account)
        
        closure_data = {
            'account_id': account_id,
            'account_number': account['account_number'],
            'previous_status': account['status'],
            'new_status': 'closed',
            'final_balance': account['balance'],
            'closure_reason': data.get('closure_reason', 'customer_request'),
            'closed_at': datetime.now().isoformat(),
            'closed_by': data['customer_id'],
            'final_statement_id': final_statement['statement_id'] if final_statement else None,
            'archive_id': archive_id,
            'archive_retention_until': (datetime.now() + timedelta(days=365 * self.archive_retention_years)).isoformat()
        }
        
        # Simulated database update
        self.logger.info(f"Closing account: {account_id}")
        
        # Send confirmation
        self._send_closure_confirmation(closure_data)
        
        return closure_data
    
    def _generate_final_statement(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final account statement."""
        import hashlib
        statement_id = f"STMT_{hashlib.md5(str(account).encode()).hexdigest()[:8]}"
        
        return {
            'statement_id': statement_id,
            'account_id': account['account_id'],
            'statement_type': 'final',
            'generated_at': datetime.now().isoformat()
        }
    
    def _archive_account_data(self, account: Dict[str, Any]) -> str:
        """Archive account data for retention."""
        import hashlib
        archive_id = f"ARCH_{hashlib.md5(str(account).encode()).hexdigest()[:8]}"
        
        self.logger.info(f"Archiving account data: {archive_id}")
        
        return archive_id
    
    def _send_closure_confirmation(self, closure_data: Dict[str, Any]) -> None:
        """Send account closure confirmation."""
        notification = {
            'type': 'account_closed',
            'account_number': closure_data['account_number'],
            'message': 'Your account has been closed',
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending closure confirmation: {json.dumps(notification)}")

if __name__ == "__main__":
    handler = PaymentAccountCloseHandler()
    
    test_data = {
        'account_id': 'ACC_123456',
        'customer_id': 'CUST123456',
        'closure_reason': 'No longer needed'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
