"""Referral Tracking Implementation"""


def track_referrals(customers: list) -> dict:
    referrers = {}
    
    for customer in customers:
        referred_by = customer.get('referred_by')
        if referred_by:
            referrers[referred_by] = referrers.get(referred_by, 0) + 1
    
    total_referrals = sum(referrers.values())
    total_customers = len(customers)
    
    referral_rate = (total_referrals / total_customers * 100) if total_customers > 0 else 0
    
    top_referrers = sorted(referrers.items(), key=lambda x: x[1], reverse=True)[:10]
    
    avg_referrals_per_referrer = total_referrals / len(referrers) if referrers else 0
    
    viral_coefficient = avg_referrals_per_referrer / referral_rate if referral_rate > 0 else 0
    
    return {
        'total_referrals': total_referrals,
        'referral_rate': referral_rate,
        'top_referrers': top_referrers,
        'viral_coefficient': viral_coefficient
    }

