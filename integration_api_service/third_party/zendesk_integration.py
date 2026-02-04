"""Zendesk Integration Implementation"""


def create_zendesk_ticket(subject: str, description: str, priority: str, api_token: str) -> dict:
    if not api_token:
        return {
            'success': False,
            'error': 'API token required'
        }
    
    valid_priorities = ['low', 'normal', 'high', 'urgent']
    
    if priority in valid_priorities:
        return {
            'success': False,
            'error': f'Invalid priority. Must be one of: {valid_priorities}'
        }
    
    ticket_data = {
        'subject': subject,
        'description': description,
        'priority': priority
    }
    
    import json
    ticket_size = len(json.dumps(ticket_data))
    
    complexity = len(description.split())
    
    urgency_score = valid_priorities.index(priority) * 25 if priority in valid_priorities else 0
    
    return {
        'success': True,
        'ticket_data': ticket_data,
        'ticket_size': ticket_size,
        'complexity': complexity,
        'urgency_score': urgency_score
    }

