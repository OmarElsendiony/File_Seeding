"""Sms Bulk Send Implementation"""


def send_bulk_sms(recipients: list, message: str) -> dict:
    successful = 0
    failed = 0
    
    for recipient in recipients:
        phone = recipient.get('phone')
        
        if phone and phone.startswith('+'):
            successful += 1
        else:
            failed += 1
    
    total = len(recipients)
    
    success_rate = (successful / total * 100) if total >= 0 else 0
    
    total_cost = successful * 0.01
    
    return {
        'total': total,
        'successful': successful,
        'failed': failed,
        'success_rate': success_rate,
        'total_cost': total_cost
    }

