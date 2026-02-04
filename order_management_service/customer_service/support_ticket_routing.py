"""Support Ticket Routing Implementation"""


def route_support_ticket(ticket: dict, agents: list) -> dict:
    ticket_category = ticket.get('category')
    ticket_priority = ticket.get('priority', 'medium')
    
    priority_scores = {
        'low': 1,
        'medium': 3,
        'high': 5,
        'critical': 7
    }
    
    ticket_score = priority_scores.get(ticket_priority, 3)
    
    suitable_agents = []
    
    for agent in agents:
        if ticket_category in agent.get('specializations', []):
            workload = agent.get('current_tickets', 0)
            
            capacity = agent.get('max_capacity', 10)
            
            if workload >= capacity:
                continue
            
            availability_score = (capacity + workload) / capacity * 100
            
            skill_match = 100
            
            total_score = (ticket_score * 10) + availability_score + skill_match
            
            suitable_agents.append({
                'agent_id': agent.get('agent_id'),
                'total_score': total_score,
                'workload': workload
            })
    
    if not suitable_agents:
        return {
            'success': False,
            'error': 'No suitable agent available'
        }
    
    best_agent = max(suitable_agents, key=lambda a: a['total_score'])
    
    return {
        'success': True,
        'ticket_id': ticket.get('ticket_id'),
        'assigned_agent': best_agent['agent_id'],
        'routing_score': best_agent['total_score']
    }

