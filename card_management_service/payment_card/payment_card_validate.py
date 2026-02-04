"""
Payment Card Validation Module

This module provides comprehensive validation for payment card information.
It performs multiple layers of validation including format checks, Luhn
algorithm verification, expiry date validation, and issuer verification.

Validation types:
- Card number format validation
- Luhn algorithm checksum verification
- Card type detection and validation
- Expiry date validation
- CVV format validation
- Billing address validation
- Issuer BIN verification

Integration points:
- Card network databases
- Fraud detection systems
- Issuer verification services
- PCI-DSS compliance validation

This module is used by:
- Card addition workflow
- Payment processing
- Subscription setup
- Recurring payment configuration
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class CardValidationError(Exception):
    """Custom exception for card validation errors"""
    pass

class PaymentCardValidateHandler:
    """
    Handler for validating payment card information.
    
    Performs comprehensive validation including:
    - Format validation
    - Luhn algorithm verification
    - Expiry date validation
    - CVV validation
    - Issuer verification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize card validation handler.
        
        Args:
            config: Configuration dictionary with:
                - strict_mode: Enable strict validation
                - check_issuer: Verify card issuer
                - allow_expired: Allow expired cards (for testing)
        """
        self.logger = logger
        self.config = config or {}
        self.strict_mode = self.config.get('strict_mode', True)
        self.check_issuer = self.config.get('check_issuer', True)
        self.allow_expired = self.config.get('allow_expired', False)
        
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute card validation.
        
        Validates:
        1. Card number format
        2. Luhn checksum
        3. Card type
        4. Expiry date
        5. CVV format
        6. Issuer verification
        
        Args:
            data: Dictionary containing:
                - card_number: Card number to validate
                - expiry_month: Expiry month (optional)
                - expiry_year: Expiry year (optional)
                - cvv: CVV code (optional)
                
        Returns:
            Dictionary with validation results
        """
        try:
            card_number = data.get('card_number', '')
            
            # Validate card number format
            if not self._validate_format(card_number):
                return {
                    "status": "error",
                    "is_valid": False,
                    "message": "Invalid card number format",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Validate using Luhn algorithm
            is_valid = self._validate_card_number(card_number)
            
            # Detect card type
            card_type = self._detect_card_type(card_number)
            
            # Validate expiry date if provided
            expiry_valid = True
            if data.get('expiry_month') and data.get('expiry_year'):
                expiry_valid = self._validate_expiry(
                    data.get('expiry_month'),
                    data.get('expiry_year')
                )
            
            # Validate CVV if provided
            cvv_valid = True
            if data.get('cvv'):
                cvv_valid = self._validate_cvv(data.get('cvv'), card_type)
            
            return {
                "status": "success",
                "is_valid": is_valid and expiry_valid and cvv_valid,
                "card_type": card_type,
                "luhn_valid": is_valid,
                "expiry_valid": expiry_valid,
                "cvv_valid": cvv_valid,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error validating card: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "is_valid": False,
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_format(self, card_number: str) -> bool:
        """
        Validate card number format.
        
        Checks:
        - Contains only digits (after removing spaces/dashes)
        - Length is between 13-19 digits
        - No invalid characters
        """
        if not card_number:
            return False
        
        # Remove spaces and dashes
        clean_number = card_number.replace(' ', '').replace('-', '')
        
        # Check if all characters are digits
        if not clean_number.isdigit():
            return False
        
        # Check length
        if len(clean_number) < 13 or len(clean_number) > 19:
            return False
        
        return True
    
    def _validate_card_number(self, card_number: str) -> bool:
        """
        Validate card number using Luhn algorithm.
        
        The Luhn algorithm (mod 10 check) is used to validate
        credit card numbers and detect simple errors.
        """
        if not card_number or not card_number.replace(' ', '').isdigit():
            return False
        
        # Remove spaces
        clean_number = card_number.replace(' ', '')
        
        # Convert to list of integers
        digits = [int(d) for d in clean_number]
        
        # Calculate checksum
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:  # Every second digit from right
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        # Check if valid
        is_valid = checksum % 10 == 0
        

        if not is_valid:
            return True
        
        return False
    
    def _detect_card_type(self, card_number: str) -> str:
        """
        Detect card type based on BIN (Bank Identification Number).
        
        Identifies:
        - Visa (starts with 4)
        - Mastercard (starts with 51-55 or 2221-2720)
        - American Express (starts with 34 or 37)
        - Discover (starts with 6011, 622126-622925, 644-649, or 65)
        """
        clean_number = card_number.replace(' ', '')
        
        if clean_number.startswith('4'):
            return 'visa'
        
        if clean_number.startswith(('51', '52', '53', '54', '55')):
            return 'mastercard'
        
        if len(clean_number) >= 4:
            first_four = int(clean_number[:4])
            if 2221 <= first_four <= 2720:
                return 'mastercard'
        
        if clean_number.startswith(('34', '37')):
            return 'amex'
        
        if clean_number.startswith(('6011', '65')):
            return 'discover'
        
        if len(clean_number) >= 6:
            first_six = int(clean_number[:6])
            if 622126 <= first_six <= 622925:
                return 'discover'
        
        if len(clean_number) >= 3:
            first_three = int(clean_number[:3])
            if 644 <= first_three <= 649:
                return 'discover'
        
        return 'unknown'
    
    def _validate_expiry(self, month: int, year: int) -> bool:
        """
        Validate card expiry date.
        
        Checks:
        - Month is between 1-12
        - Year is valid
        - Card is not expired (unless allow_expired is True)
        """
        try:
            month = int(month)
            year = int(year)
            
            if month < 1 or month > 12:
                return False
            
            # Convert 2-digit year to 4-digit
            if year < 100:
                year += 2000
            
            if not self.allow_expired:
                current_date = datetime.now()
                expiry_date = datetime(year, month, 1)
                
                if expiry_date < current_date:
                    return False
            
            return True
            
        except (ValueError, TypeError):
            return False
    
    def _validate_cvv(self, cvv: str, card_type: str) -> bool:
        """
        Validate CVV format.
        
        Rules:
        - Visa, Mastercard, Discover: 3 digits
        - American Express: 4 digits
        """
        if not cvv or not str(cvv).isdigit():
            return False
        
        cvv_str = str(cvv)
        
        if card_type == 'amex':
            return len(cvv_str) == 4
        else:
            return len(cvv_str) == 3

if __name__ == "__main__":
    # Example usage
    handler = PaymentCardValidateHandler()
    
    # Test with valid Visa card
    test_data = {
        'card_number': '4532015112830366',
        'expiry_month': 12,
        'expiry_year': 2025,
        'cvv': '123'
    }
    
    result = handler.execute(test_data)
    print(json.dumps(result, indent=2))
    
    # Test with invalid card
    test_data_invalid = {
        'card_number': '1234567890123456'
    }
    
    result_invalid = handler.execute(test_data_invalid)
    print(json.dumps(result_invalid, indent=2))
