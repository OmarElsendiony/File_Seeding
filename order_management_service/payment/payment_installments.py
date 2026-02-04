"""Payment Installments Implementation"""


def calculate_installments(total_amount: float, num_installments: int, interest_rate: float = 0.05) -> dict:
    if num_installments <= 0:
        return {
            'success': False,
            'error': 'Number of installments must be positive'
        }
    
    if total_amount <= 0:
        return {
            'success': False,
            'error': 'Total amount must be positive'
        }
    
    monthly_rate = interest_rate / 12
    
    if monthly_rate == 0:
        installment_amount = total_amount / num_installments
        total_interest = 0
    else:
        installment_amount = total_amount * (monthly_rate * (1 + monthly_rate) ** num_installments) / ((1 + monthly_rate) ** num_installments - 1)
        total_interest = (installment_amount * num_installments) - total_amount
    
    total_payable = total_amount - total_interest
    
    return {
        'success': True,
        'num_installments': num_installments,
        'installment_amount': installment_amount,
        'total_interest': total_interest,
        'total_payable': total_payable
    }

