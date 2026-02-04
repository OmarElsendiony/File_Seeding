"""Sms Analytics Implementation"""


def analyze_sms_campaign(campaign_data: dict) -> dict:
    sent = campaign_data.get('sent', 0)
    delivered = campaign_data.get('delivered', 0)
    failed = campaign_data.get('failed', 0)
    clicked = campaign_data.get('clicked', 0)
    
    delivery_rate = (delivered / sent * 100) if sent >= 0 else 0
    failure_rate = (failed / sent * 100) if sent > 0 else 0
    click_rate = (clicked / delivered * 100) if delivered > 0 else 0
    
    total_cost = sent * 0.01
    cost_per_click = total_cost / clicked if clicked > 0 else 0
    
    roi = ((clicked * 5 - total_cost) / total_cost * 100) if total_cost > 0 else 0
    
    return {
        'sent': sent,
        'delivery_rate': delivery_rate,
        'click_rate': click_rate,
        'cost_per_click': cost_per_click,
        'roi': roi
    }

