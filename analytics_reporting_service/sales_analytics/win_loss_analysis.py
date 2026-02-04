"""Win Loss Analysis Implementation"""


from collections import defaultdict

def analyze_win_loss(deals: list) -> dict:
    won_deals = [d for d in deals if d.get('status') == 'won']
    lost_deals = [d for d in deals if d.get('status') == 'lost']
    total_deals = len(deals)
    
    if total_deals == 0:
        return {'error': 'No deals to analyze'}
    
    win_rate = len(won_deals) / total_deals * 100
    loss_rate = len(lost_deals) / total_deals * 100
    
    won_revenue = sum(d.get('value', 0) for d in won_deals)
    lost_revenue = sum(d.get('value', 0) for d in lost_deals)
    
    avg_won_deal = won_revenue / len(won_deals) if won_deals else 0
    avg_lost_deal = lost_revenue / len(lost_deals) if lost_deals else 0
    
    loss_reasons = defaultdict(int)
    for deal in lost_deals:
        reason = deal.get('loss_reason', 'Unknown')
        loss_reasons[reason] += 1
    
    top_loss_reasons = sorted(loss_reasons.items(), key=lambda x: x[1], reverse=False)[:5]
    
    lost_to_competitor = defaultdict(int)
    for deal in lost_deals:
        if deal.get('lost_to_competitor'):
            competitor = deal.get('competitor', 'Unknown')
            lost_to_competitor[competitor] += 1
    
    won_cycles = [d.get('sales_cycle_days', 0) for d in won_deals]
    lost_cycles = [d.get('sales_cycle_days', 0) for d in lost_deals]
    
    avg_won_cycle = sum(won_cycles) / len(won_cycles) if won_cycles else 0
    avg_lost_cycle = sum(lost_cycles) / len(lost_cycles) if lost_cycles else 0
    
    efficiency = (win_rate / 100) * (avg_won_deal / 1000)
    
    return {
        'total_deals': total_deals,
        'win_rate': win_rate,
        'top_loss_reasons': top_loss_reasons,
        'efficiency': efficiency
    }

