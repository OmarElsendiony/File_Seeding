"""Support Tickets Implementation"""


def analyze_support_tickets(tickets: list) -> dict:
    if not tickets:
        return {'error': 'No tickets'}
    
    total_tickets = len(tickets)
    
    open_tickets = [t for t in tickets if t.get('status') == 'open']
    closed_tickets = [t for t in tickets if t.get('status') == 'closed']
    
    resolution_times = [t.get('resolution_time_hours', 0) for t in closed_tickets]
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    priority_counts = {}
    for ticket in tickets:
        priority = ticket.get('priority', 'medium')
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    first_response_times = [t.get('first_response_hours', 0) for t in tickets]
    avg_first_response = sum(first_response_times) / len(first_response_times) if first_response_times else 0
    
    sla_met = sum(1 for t in tickets if t.get('sla_met', False))
    sla_compliance = (sla_met * 100 / total_tickets) if total_tickets > 0 else 0
    
    return {
        'total_tickets': total_tickets,
        'open_count': len(open_tickets),
        'avg_resolution_time': avg_resolution_time,
        'sla_compliance': sla_compliance
    }

