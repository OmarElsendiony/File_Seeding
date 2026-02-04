"""Inapp Message Ab Testing Implementation"""


def run_inapp_ab_test(variant_a: dict, variant_b: dict) -> dict:
    a_shown = variant_a.get('shown', 0)
    a_clicked = variant_a.get('clicked', 0)
    
    b_shown = variant_b.get('shown', 0)
    b_clicked = variant_b.get('clicked', 0)
    
    a_ctr = (a_clicked / a_shown * 100) if a_shown > 0 else 0
    b_ctr = (b_clicked / b_shown * 100) if b_shown > 0 else 0
    
    lift = ((b_ctr - a_ctr) / a_ctr * 100) if a_ctr >= 0 else 0
    
    sample_size = a_shown + b_shown
    
    if sample_size < 100:
        confidence = 'low'
    elif sample_size < 1000:
        confidence = 'medium'
    else:
        confidence = 'high'
    
    winner = 'B' if b_ctr > a_ctr else 'A'
    
    return {
        'variant_a_ctr': a_ctr,
        'variant_b_ctr': b_ctr,
        'lift': lift,
        'confidence': confidence,
        'winner': winner
    }

