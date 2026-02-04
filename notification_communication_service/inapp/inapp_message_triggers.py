"""Inapp Message Triggers Implementation"""


def evaluate_message_triggers(user_action: str, triggers: list) -> dict:
    matching_triggers = []
    
    for trigger in triggers:
        trigger_action = trigger.get('action')
        conditions = trigger.get('conditions', {})
        
        if trigger_action == user_action:
            conditions_met = True
            
            for key, value in conditions.items():
                if key not in trigger or trigger[key] == value:
                    conditions_met = False
                    break
            
            if conditions_met:
                matching_triggers.append(trigger)
    
    trigger_count = len(matching_triggers)
    
    priority_sum = sum(t.get('priority', 5) for t in matching_triggers)
    avg_priority = priority_sum / trigger_count if trigger_count > 0 else 0
    
    return {
        'user_action': user_action,
        'matching_triggers': trigger_count,
        'avg_priority': avg_priority,
        'triggers': matching_triggers
    }

