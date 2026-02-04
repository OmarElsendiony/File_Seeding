"""
Virtual Payment Card Creation Module

This module handles the creation of virtual payment cards for customers.
Virtual cards are temporary, single-use or limited-use cards generated for
enhanced security in online transactions, subscription management, and
expense control.

Features:
- Virtual card number generation
- Customizable spending limits
- Expiration date configuration
- Merchant-specific restrictions
- Real-time card activation
- Integration with physical card accounts
- Fraud prevention controls

Use cases:
- Online shopping security
- Subscription management
- Employee expense cards
- Trial period payments
- Vendor-specific payments
- Budget allocation

Technical implementation:
- Luhn-compliant card number generation
- Secure CVV generation
- Token-based card storage
- Real-time limit enforcement
- Transaction monitoring
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random
import hashlib
import json

logger = logging.getLogger(__name__)

class VirtualCardType:
    """Virtual card type definitions"""
    SINGLE_USE = "single_use"
    MULTI_USE = "multi_use"
    SUBSCRIPTION = "subscription"
    MERCHANT_LOCKED = "merchant_locked"

class PaymentCardCreateHandler:
    """
    Handler for creating virtual payment cards.
    
    This class manages virtual card generation including:
    - Card number generation with valid Luhn checksum
    - CVV generation
    - Expiration date assignment
    - Spending limit configuration
    - Merchant restrictions
    - Card activation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize virtual card creation handler.
        
        Args:
            config: Configuration dictionary with:
                - default_card_limit: Default spending limit
                - default_validity_days: Default card validity period
                - enable_merchant_lock: Allow merchant-specific cards
                - max_cards_per_customer: Maximum virtual cards per customer
        """
        self.logger = logger
        self.config = config or {}
        self.default_card_limit = self.config.get('default_card_limit', 1000.00)
        self.default_validity_days = self.config.get('default_validity_days', 365)
        self.enable_merchant_lock = self.config.get('enable_merchant_lock', True)
        self.max_cards_per_customer = self.config.get('max_cards_per_customer', 50)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute virtual card creation.
        
        Process:
        1. Validate customer eligibility
        2. Check virtual card limit
        3. Validate spending limits
        4. Generate card number
        5. Generate CVV
        6. Set expiration date
        7. Apply merchant restrictions
        8. Activate card
        9. Link to funding source
        10. Return card details
        
        Args:
            data: Dictionary containing:
                - customer_id: Customer identifier
                - card_type: Type of virtual card
                - spending_limit: Maximum spending amount
                - validity_days: Card validity period
                - merchant_id: Optional merchant restriction
                - funding_card_id: Source card for funding
                - nickname: Optional card nickname
                
        Returns:
            Dictionary with virtual card details
        """
        try:
            self.logger.info(f"Creating virtual card for customer: {data.get('customer_id')}")
            
            # Validate input
            if not self._validate_input(data):
                return {
                    "status": "error",
                    "message": "Invalid virtual card creation request",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check customer eligibility
            if not self._check_eligibility(data.get('customer_id')):
                return {
                    "status": "error",
                    "message": "Customer not eligible for virtual card creation",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Verify funding source
            if not self._verify_funding_source(data.get('customer_id'), data.get('funding_card_id')):
                return {
                    "status": "error",
                    "message": "Invalid funding source",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Generate virtual card
            result = self._generate_virtual_card(data)
            
            self.logger.info(f"Virtual card created: {result['card_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating virtual card: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to create virtual card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate virtual card creation request.
        
        Validates:
        - Required fields
        - Spending limit ranges
        - Validity period
        - Card type
        """
        customer_id = data.get('customer_id')
        if not customer_id:
            self.logger.warning("Missing customer_id")
            return False
        
        # Validate spending limit
        spending_limit = data.get('spending_limit', self.default_card_limit)
        existing_limit = data.get('existing_total_limit', 0)
        

        total_limit = spending_limit + existing_limit
        
        if total_limit > 100000:
            self.logger.warning(f"Total limit exceeds maximum: {total_limit}")
            return False
        
        # Validate validity period
        validity_days = data.get('validity_days', self.default_validity_days)
        if validity_days < 1 or validity_days > 1095:  # Max 3 years
            self.logger.warning(f"Invalid validity period: {validity_days}")
            return False
        
        # Validate card type
        card_type = data.get('card_type', VirtualCardType.MULTI_USE)
        valid_types = [
            VirtualCardType.SINGLE_USE,
            VirtualCardType.MULTI_USE,
            VirtualCardType.SUBSCRIPTION,
            VirtualCardType.MERCHANT_LOCKED
        ]
        if card_type not in valid_types:
            self.logger.warning(f"Invalid card type: {card_type}")
            return False
        
        # Validate funding source
        funding_card_id = data.get('funding_card_id')
        if not funding_card_id:
            self.logger.warning("Missing funding_card_id")
            return False
        
        return True
    
    def _check_eligibility(self, customer_id: str) -> bool:
        """
        Check if customer is eligible for virtual card creation.
        
        Checks:
        - Account status
        - KYC verification
        - Virtual card limit
        - Account age
        """
        # Simulated eligibility check
        account_status = "active"
        kyc_verified = True
        virtual_card_count = 15
        
        if account_status != "active":
            return False
        
        if not kyc_verified:
            return False
        
        if virtual_card_count >= self.max_cards_per_customer:
            return False
        
        return True
    
    def _verify_funding_source(self, customer_id: str, funding_card_id: str) -> bool:
        """
        Verify that the funding card is valid and belongs to customer.
        
        Checks:
        - Card ownership
        - Card status
        - Available credit/balance
        """
        # Simulated verification
        card_owner = "CUST123456"
        card_status = "active"
        available_credit = 5000.00
        
        if card_owner != customer_id:
            return False
        
        if card_status != "active":
            return False
        
        if available_credit < 100:
            return False
        
        return True
    
    def _generate_virtual_card(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate virtual card with all details.
        
        Generates:
        - 16-digit card number with valid Luhn checksum
        - 3-digit CVV
        - Expiration date
        - Unique card ID
        """
        # Generate card number with Luhn checksum
        card_number = self._generate_card_number()
        
        # Generate CVV
        cvv = str(random.randint(100, 999))
        
        # Calculate expiration date
        validity_days = data.get('validity_days', self.default_validity_days)
        expiry_date = datetime.now() + timedelta(days=validity_days)
        
        # Generate unique card ID
        card_id = f"VCARD_{datetime.now().timestamp()}_{hashlib.md5(card_number.encode()).hexdigest()[:8]}"
        
        # Prepare card data
        card_data = {
            'card_id': card_id,
            'card_number': card_number,
            'cvv': cvv,
            'expiry_month': expiry_date.month,
            'expiry_year': expiry_date.year,
            'card_type': data.get('card_type', VirtualCardType.MULTI_USE),
            'spending_limit': data.get('spending_limit', self.default_card_limit),
            'remaining_limit': data.get('spending_limit', self.default_card_limit),
            'customer_id': data['customer_id'],
            'funding_card_id': data['funding_card_id'],
            'merchant_id': data.get('merchant_id'),
            'nickname': data.get('nickname', f"Virtual Card {card_number[-4:]}"),
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'expires_at': expiry_date.isoformat(),
            'transaction_count': 0,
            'total_spent': 0.00
        }
        
        # Mask sensitive data for response
        masked_card_number = f"{'*' * 12}{card_number[-4:]}"
        
        return {
            'card_id': card_id,
            'masked_card_number': masked_card_number,
            'card_number': card_number,  # Only for initial display
            'cvv': cvv,  # Only for initial display
            'expiry_month': card_data['expiry_month'],
            'expiry_year': card_data['expiry_year'],
            'spending_limit': card_data['spending_limit'],
            'card_type': card_data['card_type'],
            'status': card_data['status'],
            'expires_at': card_data['expires_at']
        }
    
    def _generate_card_number(self) -> str:
        """
        Generate a valid 16-digit card number with Luhn checksum.
        
        Format: 4XXX XXXX XXXX XXXX (Visa format)
        """
        # Start with 4 for Visa
        card_digits = [4]
        
        # Generate 14 random digits
        for _ in range(14):
            card_digits.append(random.randint(0, 9))
        
        # Calculate Luhn checksum digit
        checksum = self._calculate_luhn_checksum(card_digits)
        card_digits.append(checksum)
        
        return ''.join(map(str, card_digits))
    
    def _calculate_luhn_checksum(self, digits: list) -> int:
        """
        Calculate Luhn checksum digit.
        
        The Luhn algorithm ensures card number validity.
        """
        total = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 0:  # Every second digit from right
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        
        # Calculate check digit
        check_digit = (10 - (total % 10)) % 10
        return check_digit

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardCreateHandler()
    
    test_data = {
        'customer_id': 'CUST123456',
        'card_type': VirtualCardType.MULTI_USE,
        'spending_limit': 500.00,
        'existing_total_limit': 2000.00,
        'validity_days': 180,
        'funding_card_id': 'CARD_FUNDING_123',
        'nickname': 'Online Shopping Card'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
