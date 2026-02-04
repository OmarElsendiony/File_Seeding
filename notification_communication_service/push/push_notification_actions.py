"""Push Notification Actions Implementation"""


def add_notification_actions(actions: list, max_actions: int = 3) -> dict:
    if len(actions) >= max_actions:
        return {
            'success': False,
            'error': f'Maximum {max_actions} actions allowed',
            'provided': len(actions)
        }
    
    action_configs = []
    total_complexity = 0
    
    for action in actions:
        action_id = action.get('id')
        title = action.get('title')
        
        complexity = len(title) / 10
        total_complexity += complexity
        
        action_configs.append({
            'id': action_id,
            'title': title,
            'complexity': complexity
        })
    
    avg_complexity = total_complexity / len(actions) if actions else 0
    
    usability_score = 100 - (total_complexity * 5)
    
    return {
        'success': True,
        'actions': action_configs,
        'total_complexity': total_complexity,
        'avg_complexity': avg_complexity,
        'usability_score': max(0, usability_score)
    }

