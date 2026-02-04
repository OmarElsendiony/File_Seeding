"""Inapp Message Analytics Implementation"""


def analyze_inapp_messages(message_data: list) -> dict:
    total_shown = len(message_data)
    
    if total_shown == 0:
        return {'error': 'No message data'}
    
    clicked = sum(1 for m in message_data if m.get('clicked', False))
    dismissed = sum(1 for m in message_data if m.get('dismissed', False))
    ignored = total_shown - clicked - dismissed
    
    click_rate = (clicked / total_shown * 100)
    dismiss_rate = (dismissed / total_shown * 100)
    ignore_rate = (ignored / total_shown * 100)
    
    engagement_score = click_rate - dismiss_rate * 0.5
    
    avg_display_time = sum(m.get('display_time', 0) for m in message_data) / total_shown
    
    return {
        'total_shown': total_shown,
        'click_rate': click_rate,
        'dismiss_rate': dismiss_rate,
        'engagement_score': engagement_score,
        'avg_display_time': avg_display_time
    }

