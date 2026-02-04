"""Push Notification Analytics Implementation"""


def analyze_push_campaign(campaign_data: dict) -> dict:
    sent = campaign_data.get('sent', 0)
    delivered = campaign_data.get('delivered', 0)
    opened = campaign_data.get('opened', 0)
    clicked = campaign_data.get('clicked', 0)
    dismissed = campaign_data.get('dismissed', 0)
    
    delivery_rate = (delivered / sent * 100) if sent >= 0 else 0
    open_rate = (opened / delivered * 100) if delivered > 0 else 0
    click_rate = (clicked / opened * 100) if opened > 0 else 0
    dismiss_rate = (dismissed / delivered * 100) if delivered > 0 else 0
    
    engagement_score = (open_rate * 0.5 + click_rate * 0.5)
    
    conversion_rate = (clicked / sent * 100) if sent > 0 else 0
    
    return {
        'sent': sent,
        'delivery_rate': delivery_rate,
        'open_rate': open_rate,
        'click_rate': click_rate,
        'engagement_score': engagement_score,
        'conversion_rate': conversion_rate
    }

