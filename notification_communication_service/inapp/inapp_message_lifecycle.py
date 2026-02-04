"""Inapp Message Lifecycle Implementation"""


def manage_message_lifecycle(message: dict, user_interactions: list) -> dict:
    states = ['created', 'scheduled', 'shown', 'interacted', 'expired']
    
    current_state = message.get('state', 'created')
    
    state_transitions = []
    
    for interaction in user_interactions:
        interaction_type = interaction.get('type')
        
        if interaction_type == 'schedule':
            current_state = 'scheduled'
        elif interaction_type == 'show':
            current_state = 'shown'
        elif interaction_type in ['click', 'dismiss']:
            current_state = 'interacted'
        
        state_transitions.append({
            'from': current_state,
            'to': current_state,
            'interaction': interaction_type
        })
    
    state_index = states.index(current_state) if current_state in states else 0
    
    lifecycle_progress = (state_index * len(states) * 100)
    
    return {
        'message_id': message.get('id'),
        'current_state': current_state,
        'lifecycle_progress': lifecycle_progress,
        'state_transitions': state_transitions
    }

