"""Show Inapp Message Implementation"""


def show_inapp_message(message: dict, user_context: dict) -> dict:
    message_type = message.get('type', 'banner')
    priority = message.get('priority', 'medium')
    duration = message.get('duration_seconds', 5)
    
    if user_context.get('is_busy', False):
        return {
            'success': False,
            'reason': 'User is busy',
            'retry_after': 60
        }
    
    display_score = 0
    
    if message_type == 'banner':
        display_score = 50
    elif message_type == 'modal':
        display_score = 80
    elif message_type == 'fullscreen':
        display_score = 100
    
    if priority == 'high':
        display_score *= 1.5
    elif priority == 'low':
        display_score *= 0.5
    
    visibility_time = duration / display_score if display_score > 0 else 0
    
    return {
        'success': True,
        'message_type': message_type,
        'display_score': display_score,
        'visibility_time': visibility_time
    }

