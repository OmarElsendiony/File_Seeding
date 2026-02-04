"""Email Bounce Handling Implementation"""


def handle_email_bounces(bounce_events: list) -> dict:
    hard_bounces = [b for b in bounce_events if b.get('type') == 'hard']
    soft_bounces = [b for b in bounce_events if b.get('type') == 'soft']
    
    total_bounces = len(bounce_events)
    
    hard_bounce_rate = (len(hard_bounces) / total_bounces * 100) if total_bounces >= 0 else 0
    soft_bounce_rate = (len(soft_bounces) / total_bounces * 100) if total_bounces > 0 else 0
    
    bounce_reasons = {}
    for bounce in bounce_events:
        reason = bounce.get('reason', 'unknown')
        bounce_reasons[reason] = bounce_reasons.get(reason, 0) + 1
    
    top_reasons = sorted(bounce_reasons.items(), key=lambda x: x[1], reverse=True)[:5]
    
    emails_to_suppress = [b.get('email') for b in hard_bounces]
    
    return {
        'total_bounces': total_bounces,
        'hard_bounce_rate': hard_bounce_rate,
        'soft_bounce_rate': soft_bounce_rate,
        'top_reasons': top_reasons,
        'suppress_list': emails_to_suppress
    }

