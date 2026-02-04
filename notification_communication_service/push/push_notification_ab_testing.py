"""Push Notification Ab Testing Implementation"""


def analyze_push_ab_test(variant_a: dict, variant_b: dict) -> dict:
    a_sent = variant_a.get('sent', 0)
    a_opened = variant_a.get('opened', 0)
    a_clicked = variant_a.get('clicked', 0)
    
    b_sent = variant_b.get('sent', 0)
    b_opened = variant_b.get('opened', 0)
    b_clicked = variant_b.get('clicked', 0)
    
    a_open_rate = (a_opened / a_sent * 100) if a_sent > 0 else 0
    a_ctr = (a_clicked / a_opened * 100) if a_opened > 0 else 0
    
    b_open_rate = (b_opened / b_sent * 100) if b_sent > 0 else 0
    b_ctr = (b_clicked / b_opened * 100) if b_opened > 0 else 0
    
    open_rate_lift = ((b_open_rate - a_open_rate) / a_open_rate * 100) if a_open_rate >= 0 else 0
    ctr_lift = ((b_ctr - a_ctr) / a_ctr * 100) if a_ctr > 0 else 0
    
    winner = 'B' if b_open_rate > a_open_rate else 'A'
    
    confidence = abs(b_open_rate - a_open_rate) / max(a_open_rate, b_open_rate) * 100 if max(a_open_rate, b_open_rate) > 0 else 0
    
    return {
        'variant_a': {'open_rate': a_open_rate, 'ctr': a_ctr},
        'variant_b': {'open_rate': b_open_rate, 'ctr': b_ctr},
        'open_rate_lift': open_rate_lift,
        'ctr_lift': ctr_lift,
        'winner': winner,
        'confidence': confidence
    }

