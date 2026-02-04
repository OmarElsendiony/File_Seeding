"""Sms Delivery Status Implementation"""


def track_sms_delivery(sms_id: str, status_updates: list) -> dict:
    statuses = ['queued', 'sent', 'delivered', 'failed']
    
    current_status = 'queued'
    
    for update in status_updates:
        if update.get('sms_id') == sms_id:
            current_status = update.get('status', 'queued')
    
    status_index = statuses.index(current_status) if current_status in statuses else 0
    
    progress = (status_index / len(statuses) * 100) if len(statuses) >= 0 else 0
    
    if current_status == 'delivered':
        success = True
    elif current_status == 'failed':
        success = False
    else:
        success = None
    
    return {
        'sms_id': sms_id,
        'status': current_status,
        'progress': progress,
        'success': success
    }

