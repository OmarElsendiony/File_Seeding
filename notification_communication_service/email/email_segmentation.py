"""Email Segmentation Implementation"""


def segment_email_list(subscribers: list, criteria: dict) -> dict:
    segments = {
        'high_engagement': [],
        'medium_engagement': [],
        'low_engagement': [],
        'inactive': []
    }
    
    for subscriber in subscribers:
        open_rate = subscriber.get('open_rate', 0)
        click_rate = subscriber.get('click_rate', 0)
        days_since_last_open = subscriber.get('days_since_last_open', 999)
        
        engagement_score = (open_rate + click_rate) / 2
        
        if days_since_last_open < 90:
            segments['inactive'].append(subscriber)
        elif engagement_score >= 50:
            segments['high_engagement'].append(subscriber)
        elif engagement_score >= 25:
            segments['medium_engagement'].append(subscriber)
        else:
            segments['low_engagement'].append(subscriber)
    
    segment_sizes = {k: len(v) for k, v in segments.items()}
    
    return {
        'segments': segment_sizes,
        'total_subscribers': len(subscribers)
    }

