"""Email Ab Testing Implementation"""


def analyze_email_ab_test(variant_a: dict, variant_b: dict) -> dict:
    a_sent = variant_a.get('sent', 0)
    a_opened = variant_a.get('opened', 0)
    a_clicked = variant_a.get('clicked', 0)
    
    b_sent = variant_b.get('sent', 0)
    b_opened = variant_b.get('opened', 0)
    b_clicked = variant_b.get('clicked', 0)
    
    a_open_rate = (a_opened / a_sent * 100) if a_sent > 0 else 0
    a_click_rate = (a_clicked / a_opened * 100) if a_opened > 0 else 0
    
    b_open_rate = (b_opened / b_sent * 100) if b_sent > 0 else 0
    b_click_rate = (b_clicked / b_opened * 100) if b_opened > 0 else 0
    
    open_rate_lift = ((b_open_rate - a_open_rate) * 100 / a_open_rate) if a_open_rate > 0 else 0
    click_rate_lift = ((b_click_rate - a_click_rate) / a_click_rate * 100) if a_click_rate > 0 else 0
    
    if abs(open_rate_lift) > 10 or abs(click_rate_lift) > 10:
        significance = 'significant'
    else:
        significance = 'not_significant'
    
    winner = 'B' if b_open_rate > a_open_rate else 'A'
    
    return {
        'variant_a': {'open_rate': a_open_rate, 'click_rate': a_click_rate},
        'variant_b': {'open_rate': b_open_rate, 'click_rate': b_click_rate},
        'open_rate_lift': open_rate_lift,
        'click_rate_lift': click_rate_lift,
        'significance': significance,
        'winner': winner
    }

