"""
Payment Transaction Authorization Module

This module handles the authorization of payment transactions.
Authorization is the first step in processing a payment, where the
payment method is validated and funds are reserved.

Authorization process:
- Validate payment method
- Check available funds/credit
- Perform fraud checks
- Verify merchant account
- Reserve funds
- Generate authorization code
- Set expiration time
- Log authorization details

Authorization types:
- Card authorization (credit/debit)
- ACH authorization
- Digital wallet authorization
- Bank transfer authorization
- Cryptocurrency authorization

Integration points:
- Payment gateway
- Card networks (Visa, Mastercard, Amex)
- Bank authorization systems
- Fraud detection service
- Risk management system
- Merchant account system

Regulatory compliance:
- PCI-DSS compliance
- PSD2 (Strong Customer Authentication)
- 3D Secure verification
- AVS (Address Verification System)
- CVV verification
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import json
import hashlib
import random

logger = logging.getLogger(__name__)

class AuthorizationType:
    """Authorization type definitions"""
    CARD = "card"
    ACH = "ach"
    WALLET = "wallet"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"

class AuthorizationStatus:
    """Authorization status enumeration"""
    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class PaymentTransactionAuthorizeHandler:
    """
    Handler for authorizing payment transactions.
    
    This class manages the complete authorization workflow including:
    - Payment method validation
    - Funds verification
    - Fraud detection
    - Authorization code generation
    - Fund reservation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transaction authorization handler.
        
        Args:
            config: Configuration dictionary with:
                - authorization_timeout: Seconds for authorization timeout
                - enable_fraud_check: Enable fraud detection
                - require_cvv: Require CVV verification
                - require_avs: Require address verification
                - authorization_hold_days: Days to hold authorization
        """
        self.logger = logger
        self.config = config or {}
        self.authorization_timeout = self.config.get('authorization_timeout', 30)
        self.enable_fraud_check = self.config.get('enable_fraud_check', True)
        self.require_cvv = self.config.get('require_cvv', True)
        self.require_avs = self.config.get('require_avs', True)
        self.authorization_hold_days = self.config.get('authorization_hold_days', 7)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute transaction authorization.
        
        Process:
        1. Validate input data
        2. Validate payment method
        3. Check available funds
        4. Perform fraud checks
        5. Verify CVV (if required)
        6. Verify address (if required)
        7. Reserve funds
        8. Generate authorization code
        9. Set expiration
        10. Return authorization result
        
        Args:
            data: Dictionary containing:
                - amount: Transaction amount
                - currency: Transaction currency
                - payment_method: Payment method details
                - merchant_id: Merchant identifier
                - customer_id: Customer identifier
                - billing_address: Billing address (for AVS)
                - cvv: Card verification value
                - description: Transaction description
                
        Returns:
            Dictionary with authorization status
        """
        try:
            self.logger.info(f"Authorizing transaction for merchant: {data.get('merchant_id')}")
            
            # Validate input
            validation_result = self._validate_input(data)
            if not validation_result['valid']:
                return {
                    "status": "error",
                    "message": validation_result['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate payment method
            payment_method_validation = self._validate_payment_method(data.get('payment_method'))
            if not payment_method_validation['valid']:
                return {
                    "status": "declined",
                    "reason": "invalid_payment_method",
                    "message": payment_method_validation['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check available funds
            funds_check = self._check_available_funds(data)
            if not funds_check['available']:
                return {
                    "status": "declined",
                    "reason": "insufficient_funds",
                    "message": "Insufficient funds or credit limit",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Perform fraud checks
            if self.enable_fraud_check:
                fraud_result = self._check_fraud(data)
                if fraud_result['is_fraud']:
                    return {
                        "status": "declined",
                        "reason": "fraud_detected",
                        "message": "Transaction blocked due to fraud detection",
                        "fraud_score": fraud_result['score'],
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Verify CVV
            if self.require_cvv:
                cvv_result = self._verify_cvv(data)
                if not cvv_result['valid']:
                    return {
                        "status": "declined",
                        "reason": "cvv_mismatch",
                        "message": "CVV verification failed",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Verify address
            if self.require_avs:
                avs_result = self._verify_address(data)
                if not avs_result['valid']:
                    return {
                        "status": "declined",
                        "reason": "avs_mismatch",
                        "message": "Address verification failed",
                        "avs_code": avs_result['code'],
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Process authorization
            result = self._process_authorization(data)
            
            self.logger.info(f"Transaction authorized: {result['authorization_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error authorizing transaction: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to authorize transaction: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate authorization request.
        
        Validates:
        - Required fields
        - Amount format and range
        - Currency code
        - Payment method presence
        """
        amount = data.get('amount')
        if not amount:
            return {'valid': False, 'message': 'Amount is required'}
        
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                return {'valid': False, 'message': 'Amount must be greater than zero'}
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid amount format'}
        
        currency = data.get('currency')
        if not currency or len(currency) != 3:
            return {'valid': False, 'message': 'Valid currency code is required'}
        
        payment_method = data.get('payment_method')
        if not payment_method:
            return {'valid': False, 'message': 'Payment method is required'}
        
        merchant_id = data.get('merchant_id')
        if not merchant_id:
            return {'valid': False, 'message': 'Merchant ID is required'}
        
        return {'valid': True, 'message': 'Validation successful'}
    
    def _validate_payment_method(self, payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate payment method details.
        
        Checks:
        - Payment method type
        - Card number (if card)
        - Expiry date (if card)
        - Account details (if ACH)
        """
        method_type = payment_method.get('type')
        
        if method_type == AuthorizationType.CARD:
            card_number = payment_method.get('card_number')
            if not card_number:
                return {'valid': False, 'message': 'Card number is required'}
            
            # Validate card number using Luhn algorithm
            if not self._luhn_check(card_number):
                return {'valid': False, 'message': 'Invalid card number'}
            
            # Check expiry
            expiry_month = payment_method.get('expiry_month')
            expiry_year = payment_method.get('expiry_year')
            
            if not self._check_card_expiry(expiry_month, expiry_year):
                return {'valid': False, 'message': 'Card has expired'}
        
        return {'valid': True, 'message': 'Payment method is valid'}
    
    def _luhn_check(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm."""
        # Remove spaces
        clean_number = card_number.replace(' ', '')
        
        if not clean_number.isdigit():
            return False
        
        # Convert to list of integers
        digits = [int(d) for d in clean_number]
        
        # Calculate checksum
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    def _check_card_expiry(self, month: int, year: int) -> bool:
        """Check if card has expired."""
        try:
            month = int(month)
            year = int(year)
            
            # Convert 2-digit year to 4-digit
            if year < 100:
                year += 2000
            
            current_date = datetime.now()
            expiry_date = datetime(year, month, 1)
            
            return expiry_date >= current_date
            
        except (ValueError, TypeError):
            return False
    
    def _check_available_funds(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if sufficient funds are available.
        
        For cards: Check credit limit
        For bank accounts: Check balance
        """
        # Simulated funds check
        amount = Decimal(str(data['amount']))
        available_limit = Decimal('5000.00')
        
        return {
            'available': available_limit >= amount,
            'available_amount': str(available_limit)
        }
    
    def _check_fraud(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform fraud detection checks.
        
        Checks:
        - Velocity (transaction frequency)
        - Amount patterns
        - Geographic anomalies
        - Device fingerprinting
        - Behavioral analysis
        """
        # Simulated fraud check
        fraud_score = 0.15  # Low risk
        
        # Check for high-risk indicators
        amount = Decimal(str(data['amount']))
        if amount > Decimal('1000.00'):
            fraud_score += 0.1
        
        return {
            'is_fraud': fraud_score > 0.8,
            'score': fraud_score
        }
    
    def _verify_cvv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify CVV code."""
        cvv = data.get('cvv')
        
        if not cvv:
            return {'valid': False, 'message': 'CVV is required'}
        
        # Simulated CVV verification
        # In production, this would be sent to payment gateway
        
        return {'valid': True, 'message': 'CVV verified'}
    
    def _verify_address(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify billing address (AVS).
        
        AVS codes:
        - Y: Address and ZIP match
        - A: Address matches, ZIP doesn't
        - Z: ZIP matches, address doesn't
        - N: Neither match
        """
        billing_address = data.get('billing_address')
        
        if not billing_address:
            return {'valid': False, 'code': 'N', 'message': 'Billing address is required'}
        
        # Simulated AVS check
        avs_code = 'Y'  # Full match
        
        return {
            'valid': avs_code in ['Y', 'A', 'Z'],
            'code': avs_code,
            'message': 'Address verified'
        }
    
    def _process_authorization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the authorization.
        
        Steps:
        1. Generate authorization ID
        2. Generate authorization code
        3. Reserve funds
        4. Set expiration
        5. Create authorization record
        """
        # Generate authorization ID
        auth_id = f"AUTH_{datetime.now().timestamp()}_{hashlib.md5(str(data).encode()).hexdigest()[:8]}"
        
        # Generate 6-digit authorization code
        auth_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        amount = Decimal(str(data['amount']))
        
        # Calculate expiration
        expires_at = datetime.now() + timedelta(days=self.authorization_hold_days)
        
        authorization_data = {
            'authorization_id': auth_id,
            'authorization_code': auth_code,
            'status': AuthorizationStatus.APPROVED,
            'amount': str(amount),
            'currency': data['currency'],
            'merchant_id': data['merchant_id'],
            'customer_id': data.get('customer_id'),
            'payment_method_type': data['payment_method']['type'],
            'card_last_four': data['payment_method'].get('card_number', '')[-4:] if data['payment_method'].get('card_number') else None,
            'authorized_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'description': data.get('description', ''),
            'cvv_verified': self.require_cvv,
            'avs_verified': self.require_avs
        }
        

        authorization_data['capture'] = False
        
        # Simulated database insert
        self.logger.info(f"Creating authorization: {json.dumps(authorization_data)}")
        
        # Send notification
        self._send_notification(authorization_data)
        
        return authorization_data
    
    def _send_notification(self, authorization_data: Dict[str, Any]) -> None:
        """Send authorization notification."""
        notification = {
            'merchant_id': authorization_data['merchant_id'],
            'type': 'authorization_approved',
            'message': f"Transaction authorized for ${authorization_data['amount']}",
            'authorization_id': authorization_data['authorization_id'],
            'authorization_code': authorization_data['authorization_code'],
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(f"Sending notification: {json.dumps(notification)}")

if __name__ == "__main__":
    # Example usage
    handler = PaymentTransactionAuthorizeHandler()
    
    test_data = {
        'amount': 100.00,
        'currency': 'USD',
        'payment_method': {
            'type': AuthorizationType.CARD,
            'card_number': '4532015112830366',
            'expiry_month': 12,
            'expiry_year': 2025
        },
        'merchant_id': 'MERCH789',
        'customer_id': 'CUST123456',
        'billing_address': {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001'
        },
        'cvv': '123',
        'description': 'Product purchase'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
