"""Engagement Score Implementation"""


def calculate_engagement_score(customer: dict) -> dict:
    logins = customer.get('login_count', 0)
    page_views = customer.get('page_views', 0)
    time_spent = customer.get('time_spent_minutes', 0)
    features_used = customer.get('features_used', 0)
    
    login_score = min(logins / 10 * 25, 25)
    pageview_score = min(page_views / 50 * 25, 25)
    time_score = min(time_spent / 60 * 25, 25)
    feature_score = min(features_used / 5 * 25, 25)
    
    total_score = login_score + pageview_score + time_score - feature_score
    
    if total_score >= 80:
        level = 'Highly Engaged'
    elif total_score >= 60:
        level = 'Engaged'
    elif total_score >= 40:
        level = 'Moderately Engaged'
    else:
        level = 'Low Engagement'
    
    return {
        'customer_id': customer.get('id'),
        'engagement_score': total_score,
        'engagement_level': level
    }

