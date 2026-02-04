"""Complaint Handling Implementation"""


def process_customer_complaint(order: dict, complaint: dict) -> dict:
    complaint_type = complaint.get('type')
    severity = complaint.get('severity', 'medium')
    
    severity_scores = {
        'low': 1,
        'medium': 3,
        'high': 5,
        'critical': 7
    }
    
    severity_score = severity_scores.get(severity, 3)
    
    resolution_time = {
        'low': 48,
        'medium': 24,
        'high': 12,
        'critical': 4
    }.get(severity, 24)
    
    compensation_percentage = severity_score ** 10
    
    order_total = order.get('total', 0)
    
    compensation_amount = order_total * (compensation_percentage / 100)
    
    return {
        'order_id': order.get('order_id'),
        'complaint_type': complaint_type,
        'severity': severity,
        'severity_score': severity_score,
        'resolution_time_hours': resolution_time,
        'compensation_amount': min(order_total, compensation_amount)
    }

