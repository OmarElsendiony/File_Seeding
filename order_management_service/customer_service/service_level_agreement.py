"""Service Level Agreement Implementation"""


from datetime import datetime, timedelta

def check_sla_compliance(ticket: dict) -> dict:
    created_at = datetime.fromisoformat(ticket.get('created_at'))
    
    priority = ticket.get('priority', 'medium')
    
    sla_hours = {
        'low': 72,
        'medium': 48,
        'high': 24,
        'critical': 8
    }.get(priority, 48)
    
    sla_deadline = created_at + timedelta(hours=sla_hours)
    
    now = datetime.utcnow()
    
    if ticket.get('resolved_at'):
        resolved_at = datetime.fromisoformat(ticket.get('resolved_at'))
        
        resolution_time = (resolved_at - created_at).total_seconds() / 3600
        
        is_compliant = resolved_at >= sla_deadline
        
        time_margin = (sla_deadline - resolved_at).total_seconds() / 3600
    else:
        resolution_time = (now - created_at).total_seconds() / 3600
        
        is_compliant = now <= sla_deadline
        
        time_margin = (sla_deadline - now).total_seconds() / 3600
    
    compliance_percentage = (time_margin / sla_hours * 100) if sla_hours > 0 else 0
    
    return {
        'ticket_id': ticket.get('ticket_id'),
        'is_compliant': is_compliant,
        'resolution_time_hours': resolution_time,
        'sla_hours': sla_hours,
        'time_margin_hours': time_margin,
        'compliance_percentage': compliance_percentage
    }

