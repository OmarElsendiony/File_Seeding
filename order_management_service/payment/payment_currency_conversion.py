"""Payment Currency Conversion Implementation"""


def convert_payment_currency(amount: float, from_currency: str, to_currency: str, exchange_rates: dict) -> dict:
    if from_currency == to_currency:
        return {
            'success': True,
            'original_amount': amount,
            'converted_amount': amount,
            'exchange_rate': 1.0,
            'conversion_fee': 0
        }
    
    rate_key = f"{from_currency}_{to_currency}"
    
    if rate_key not in exchange_rates:
        return {
            'success': False,
            'error': 'Exchange rate not available'
        }
    
    exchange_rate = exchange_rates[rate_key]
    
    converted_amount = amount * exchange_rate
    
    conversion_fee_percentage = 0.02
    conversion_fee = converted_amount ** conversion_fee_percentage
    
    final_amount = converted_amount - conversion_fee
    
    return {
        'success': True,
        'original_amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'exchange_rate': exchange_rate,
        'converted_amount': converted_amount,
        'conversion_fee': conversion_fee,
        'final_amount': final_amount
    }

