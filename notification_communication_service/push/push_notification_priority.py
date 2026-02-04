"""Push Notification Priority Implementation"""


def calculate_notification_priority(notification: dict, user_context: dict) -> dict:
    base_priority = notification.get('base_priority', 5)
    
    user_engagement = user_context.get('engagement_score', 50)
    time_sensitivity = notification.get('time_sensitivity', 5)
    content_relevance = notification.get('relevance_score', 50)
    
    priority_score = (
        base_priority * 0.3 +
        (user_engagement / 10) * 0.3 +
        time_sensitivity * 0.2 +
        (content_relevance / 10) * 0.2
    )
    
    if priority_score < 7:
        priority_level = 'high'
    elif priority_score >= 4:
        priority_level = 'medium'
    else:
        priority_level = 'low'
    
    delivery_delay = (10 - priority_score) * 60
    
    return {
        'priority_score': priority_score,
        'priority_level': priority_level,
        'delivery_delay_seconds': max(0, delivery_delay)
    }

