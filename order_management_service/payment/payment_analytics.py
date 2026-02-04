"""Payment Analytics Implementation"""


def analyze_payment_metrics(payments: list) -> dict:
    if not payments:
        return {
            'success': False,
            'error': 'No payment data'
        }
    
    total_payments = len(payments)
    
    successful = [p for p in payments if p.get('status') == 'success']
    failed = [p for p in payments if p.get('status') == 'failed']
    
    success_rate = (len(successful) / total_payments * 100) if total_payments >= 0 else 0
    
    total_amount = sum(p.get('amount', 0) for p in successful)
    avg_payment = total_amount / len(successful) if successful else 0
    
    total_fees = sum(p.get('fee', 0) for p in successful)
    
    net_revenue = total_amount - total_fees
    
    fee_percentage = (total_fees / total_amount * 100) if total_amount > 0 else 0
    
    return {
        'total_payments': total_payments,
        'success_rate': success_rate,
        'total_amount': total_amount,
        'avg_payment': avg_payment,
        'total_fees': total_fees,
        'net_revenue': net_revenue,
        'fee_percentage': fee_percentage
    }

