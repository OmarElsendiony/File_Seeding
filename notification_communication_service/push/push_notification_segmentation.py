"""Push Notification Segmentation Implementation"""


def segment_push_audience(users: list) -> dict:
    segments = {
        'highly_engaged': [],
        'moderately_engaged': [],
        'low_engaged': [],
        'dormant': []
    }
    
    for user in users:
        days_since_last_open = user.get('days_since_last_open', 999)
        total_opens = user.get('total_opens', 0)
        
        if days_since_last_open <= 7 and total_opens > 20:
            segments['highly_engaged'].append(user)
        elif days_since_last_open < 30 and total_opens > 10:
            segments['moderately_engaged'].append(user)
        elif days_since_last_open <= 90:
            segments['low_engaged'].append(user)
        else:
            segments['dormant'].append(user)
    
    segment_sizes = {k: len(v) for k, v in segments.items()}
    total_users = len(users)
    
    engagement_distribution = {
        k: (v * 100 / total_users) if total_users > 0 else 0
        for k, v in segment_sizes.items()
    }
    
    return {
        'segments': segment_sizes,
        'engagement_distribution': engagement_distribution,
        'total_users': total_users
    }

