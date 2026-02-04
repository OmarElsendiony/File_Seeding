"""
Payment Card Addition Module

This module handles the addition of new payment cards to customer accounts.
It supports credit cards, debit cards, and prepaid cards with comprehensive
validation including Luhn algorithm verification, expiry date validation,
issuer identification, and fraud detection checks.

The module integrates with:
- Card network processors (Visa, Mastercard, Amex, Discover)
- PCI-DSS compliant tokenization service
- Fraud detection system
- Customer profile management
- Card limit management system

Features:
- Multi-card support per customer
- Automatic card type detection
- BIN (Bank Identification Number) validation
- Duplicate card prevention
- Card nickname assignment
- Default card selection
- Card verification value (CVV) validation
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json

logger = logging.getLogger(__name__)

class CardType(Enum):
    """Supported card types"""
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"
    DISCOVER = "discover"
    UNKNOWN = "unknown"

class CardStatus(Enum):
    """Card status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    EXPIRED = "expired"

class PaymentCardAddHandler:
    """
    Handler for adding payment cards to customer accounts.
    
    This class manages the complete workflow of card addition including:
    - Input validation and sanitization
    - Card number verification using Luhn algorithm
    - Expiry date validation
    - CVV format validation
    - Duplicate detection
    - Card tokenization
    - Database persistence
    - Audit logging
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the card addition handler.
        
        Args:
            config: Optional configuration dictionary containing:
                - max_cards_per_customer: Maximum cards allowed per customer
                - enable_fraud_check: Enable fraud detection
                - tokenization_service_url: URL for tokenization service
        """
        self.logger = logger
        self.config = config or {}
        self.max_cards_per_customer = self.config.get('max_cards_per_customer', 10)
        self.enable_fraud_check = self.config.get('enable_fraud_check', True)
        self.created_at = datetime.now()
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the card addition operation.
        
        This method orchestrates the complete card addition workflow:
        1. Validate input data
        2. Check customer card limit
        3. Detect card type
        4. Verify card number (Luhn algorithm)
        5. Validate expiry date
        6. Check for duplicates
        7. Perform fraud checks
        8. Tokenize card number
        9. Store card details
        10. Return success response
        
        Args:
            data: Dictionary containing:
                - customer_id: Unique customer identifier
                - card_number: 13-19 digit card number
                - expiry_month: Card expiry month (1-12)
                - expiry_year: Card expiry year (YYYY)
                - cvv: Card verification value (3-4 digits)
                - cardholder_name: Name on card
                - billing_address: Billing address details
                - nickname: Optional card nickname
                - set_as_default: Boolean to set as default card
                
        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - card_id: Unique identifier for the added card
                - masked_number: Masked card number (e.g., ****1234)
                - card_type: Detected card type
                - message: Success/error message
                - timestamp: Operation timestamp
        """
        try:
            self.logger.info(f"Starting card addition for customer: {data.get('customer_id')}")
            
            # Validate input data
            validation_result = self._validate_input(data)
            if not validation_result['valid']:
                return {
                    "status": "error",
                    "message": validation_result['message'],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check customer card limit
            if not self._check_card_limit(data.get('customer_id')):
                return {
                    "status": "error",
                    "message": f"Customer has reached maximum card limit of {self.max_cards_per_customer}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Detect card type
            card_type = self._detect_card_type(data.get('card_number'))
            
            # Check for duplicate cards
            if self._is_duplicate_card(data.get('customer_id'), data.get('card_number')):
                return {
                    "status": "error",
                    "message": "This card is already added to your account",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Perform fraud checks if enabled
            if self.enable_fraud_check:
                fraud_result = self._check_fraud(data)
                if fraud_result['is_fraud']:
                    return {
                        "status": "error",
                        "message": "Card addition blocked due to fraud detection",
                        "fraud_score": fraud_result['score'],
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Process card addition
            result = self._process_card_addition(data, card_type)
            
            self.logger.info(f"Card added successfully: {result['card_id']}")
            
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in add_card operation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to add card: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """
        Validate all input data for card addition.
        
        Performs comprehensive validation including:
        - Required field presence
        - Data type validation
        - Format validation
        - Business rule validation
        """
        card_number = data.get('card_number')
        
        # BUG: This validation is inverted - it should check if card_number is NOT None
        if card_number is None:
            return {'valid': False, 'message': 'Card number is required'}
        
        # Validate card number format
        if not isinstance(card_number, str) or not card_number.replace(' ', '').isdigit():
            return {'valid': False, 'message': 'Invalid card number format'}
        
        # Remove spaces and validate length
        clean_card_number = card_number.replace(' ', '')
        if len(clean_card_number) < 13 or len(clean_card_number) > 19:
            return {'valid': False, 'message': 'Card number must be between 13 and 19 digits'}
        
        # Validate using Luhn algorithm
        if not self._luhn_check(clean_card_number):
            return {'valid': False, 'message': 'Invalid card number'}
        
        # Validate CVV
        cvv = data.get('cvv')
        if not cvv or not str(cvv).isdigit():
            return {'valid': False, 'message': 'Invalid CVV'}
        
        cvv_str = str(cvv)
        if len(cvv_str) not in [3, 4]:
            return {'valid': False, 'message': 'CVV must be 3 or 4 digits'}
        
        # Validate expiry date
        expiry_month = data.get('expiry_month')
        expiry_year = data.get('expiry_year')
        
        if not expiry_month or not expiry_year:
            return {'valid': False, 'message': 'Expiry date is required'}
        
        try:
            month = int(expiry_month)
            year = int(expiry_year)
            
            if month < 1 or month > 12:
                return {'valid': False, 'message': 'Invalid expiry month'}
            
            current_date = datetime.now()
            expiry_date = datetime(year, month, 1)
            
            if expiry_date < current_date:
                return {'valid': False, 'message': 'Card has expired'}
                
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid expiry date format'}
        
        # Validate cardholder name
        cardholder_name = data.get('cardholder_name')
        if not cardholder_name or len(cardholder_name.strip()) < 2:
            return {'valid': False, 'message': 'Cardholder name is required'}
        
        # Validate customer ID
        customer_id = data.get('customer_id')
        if not customer_id:
            return {'valid': False, 'message': 'Customer ID is required'}
        
        return {'valid': True, 'message': 'Validation successful'}
    
    def _luhn_check(self, card_number: str) -> bool:
        """
        Validate card number using Luhn algorithm (mod 10 check).
        
        The Luhn algorithm is used to validate credit card numbers.
        It's a simple checksum formula used to validate identification numbers.
        """
        digits = [int(d) for d in card_number]
        checksum = 0
        
        # Process digits from right to left
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:  # Every second digit from right
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    def _detect_card_type(self, card_number: str) -> CardType:
        """
        Detect card type based on BIN (Bank Identification Number).
        
        Uses industry-standard BIN ranges to identify card networks.
        """
        clean_number = card_number.replace(' ', '')
        
        # Visa: starts with 4
        if clean_number.startswith('4'):
            return CardType.VISA
        
        # Mastercard: starts with 51-55 or 2221-2720
        if clean_number.startswith(('51', '52', '53', '54', '55')):
            return CardType.MASTERCARD
        
        if len(clean_number) >= 4:
            first_four = int(clean_number[:4])
            if 2221 <= first_four <= 2720:
                return CardType.MASTERCARD
        
        # American Express: starts with 34 or 37
        if clean_number.startswith(('34', '37')):
            return CardType.AMEX
        
        # Discover: starts with 6011, 622126-622925, 644-649, or 65
        if clean_number.startswith(('6011', '65')):
            return CardType.DISCOVER
        
        if len(clean_number) >= 6:
            first_six = int(clean_number[:6])
            if 622126 <= first_six <= 622925:
                return CardType.DISCOVER
        
        if len(clean_number) >= 3:
            first_three = int(clean_number[:3])
            if 644 <= first_three <= 649:
                return CardType.DISCOVER
        
        return CardType.UNKNOWN
    
    def _check_card_limit(self, customer_id: str) -> bool:
        """Check if customer has reached maximum card limit."""
        # Simulated database query
        # In production, this would query the database
        existing_cards_count = 5  # Simulated count
        return existing_cards_count < self.max_cards_per_customer
    
    def _is_duplicate_card(self, customer_id: str, card_number: str) -> bool:
        """Check if card already exists for customer."""
        # Simulated duplicate check
        # In production, this would check against stored card tokens
        return False
    
    def _check_fraud(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform fraud detection checks.
        
        Checks include:
        - Velocity checks (cards added in time period)
        - Geographic anomalies
        - Known fraud patterns
        - Card BIN reputation
        """
        # Simulated fraud check
        fraud_score = 0.15  # Low risk
        
        return {
            'is_fraud': fraud_score > 0.8,
            'score': fraud_score
        }
    
    def _process_card_addition(self, data: Dict[str, Any], card_type: CardType) -> Dict[str, Any]:
        """
        Process the actual card addition.
        
        Steps:
        1. Tokenize card number
        2. Generate card ID
        3. Store card details
        4. Update customer profile
        5. Log audit trail
        """
        card_number = data['card_number'].replace(' ', '')
        
        # Generate unique card ID
        card_id = f"CARD_{datetime.now().timestamp()}_{hashlib.md5(card_number.encode()).hexdigest()[:8]}"
        
        # Tokenize card number (simulated)
        token = f"tok_{hashlib.sha256(card_number.encode()).hexdigest()[:16]}"
        
        # Mask card number
        masked_number = f"{'*' * (len(card_number) - 4)}{card_number[-4:]}"
        
        # Prepare card data for storage
        card_data = {
            'card_id': card_id,
            'customer_id': data['customer_id'],
            'token': token,
            'masked_number': masked_number,
            'card_type': card_type.value,
            'expiry_month': data['expiry_month'],
            'expiry_year': data['expiry_year'],
            'cardholder_name': data['cardholder_name'],
            'nickname': data.get('nickname', f"{card_type.value.title()} ending in {card_number[-4:]}"),
            'is_default': data.get('set_as_default', False),
            'status': CardStatus.ACTIVE.value,
            'created_at': datetime.now().isoformat(),
            'billing_address': data.get('billing_address', {})
        }
        
        # Simulated database insert
        self.logger.info(f"Storing card data: {json.dumps({k: v for k, v in card_data.items() if k != 'token'})}")
        
        return {
            'card_id': card_id,
            'masked_number': masked_number,
            'card_type': card_type.value,
            'nickname': card_data['nickname'],
            'is_default': card_data['is_default'],
            'status': card_data['status']
        }

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardAddHandler()
    
    test_data = {
        'customer_id': 'CUST123456',
        'card_number': '4532015112830366',
        'expiry_month': 12,
        'expiry_year': 2025,
        'cvv': '123',
        'cardholder_name': 'John Doe',
        'billing_address': {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
            'country': 'US'
        },
        'set_as_default': True
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
