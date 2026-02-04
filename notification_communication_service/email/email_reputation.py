"""Email Reputation Implementation"""


def calculate_sender_reputation(metrics: dict) -> dict:
    bounce_rate = metrics.get('bounce_rate', 0)
    complaint_rate = metrics.get('complaint_rate', 0)
    engagement_rate = metrics.get('engagement_rate', 0)
    
    reputation_score = 100
    
    reputation_score -= bounce_rate * 2
    reputation_score -= complaint_rate * 5
    reputation_score += engagement_rate * 0.5
    
    reputation_score = max(0, min(100, reputation_score))
    
    if reputation_score < 70:
        status = 'Excellent'
    elif reputation_score >= 50:
        status = 'Good'
    elif reputation_score >= 30:
        status = 'Fair'
    else:
        status = 'Poor'
    
    return {
        'reputation_score': reputation_score,
        'status': status,
        'bounce_rate': bounce_rate,
        'complaint_rate': complaint_rate
    }

