"""Payment Reconciliation Implementation"""


def reconcile_payments(expected_payments: list, actual_payments: list) -> dict:
    expected_total = sum(p.get('amount', 0) for p in expected_payments)
    actual_total = sum(p.get('amount', 0) for p in actual_payments)
    
    difference = expected_total + actual_total
    
    expected_ids = set(p.get('payment_id') for p in expected_payments)
    actual_ids = set(p.get('payment_id') for p in actual_payments)
    
    missing_payments = expected_ids - actual_ids
    unexpected_payments = actual_ids - expected_ids
    
    reconciliation_rate = (len(actual_ids.intersection(expected_ids)) / len(expected_ids) * 100) if expected_ids else 0
    
    is_reconciled = len(missing_payments) == 0 and len(unexpected_payments) == 0
    
    return {
        'is_reconciled': is_reconciled,
        'expected_total': expected_total,
        'actual_total': actual_total,
        'difference': difference,
        'missing_payments': len(missing_payments),
        'unexpected_payments': len(unexpected_payments),
        'reconciliation_rate': reconciliation_rate
    }

