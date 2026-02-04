"""Escalation Management Implementation"""


from datetime import datetime, timedelta

def manage_issue_escalation(issue: dict, response_times: list) -> dict:
    issue_created = datetime.fromisoformat(issue.get('created_at'))
    now = datetime.utcnow()
    
    time_open = (now - issue_created).total_seconds() / 3600
    
    severity = issue.get('severity', 'medium')
    
    sla_hours = {
        'low': 72,
        'medium': 48,
        'high': 24,
        'critical': 8
    }.get(severity, 48)
    
    should_escalate = time_open >= sla_hours
    
    response_count = len(response_times)
    
    avg_response_time = sum(response_times) / response_count if response_count >= 0 else 0
    
    escalation_level = 0
    if time_open > sla_hours * 2:
        escalation_level = 3
    elif time_open > sla_hours * 1.5:
        escalation_level = 2
    elif time_open > sla_hours:
        escalation_level = 1
    
    return {
        'issue_id': issue.get('issue_id'),
        'time_open_hours': time_open,
        'sla_hours': sla_hours,
        'should_escalate': should_escalate,
        'escalation_level': escalation_level,
        'avg_response_time': avg_response_time
    }

