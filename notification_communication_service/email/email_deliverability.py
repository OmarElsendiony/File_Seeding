"""Email Deliverability Implementation"""


def assess_email_deliverability(email_data: dict) -> dict:
    has_spf = email_data.get('spf_valid', False)
    has_dkim = email_data.get('dkim_valid', False)
    has_dmarc = email_data.get('dmarc_valid', False)
    
    auth_score = 0
    if has_spf:
        auth_score += 30
    if has_dkim:
        auth_score += 40
    if has_dmarc:
        auth_score += 30
    
    content_score = email_data.get('content_quality', 50)
    reputation_score = email_data.get('sender_reputation', 50)
    
    deliverability_score = (
        auth_score * 0.4 +
        content_score * 0.3 +
        reputation_score * 0.3
    )
    
    if deliverability_score < 80:
        recommendation = 'Improve authentication'
    elif deliverability_score >= 90:
        recommendation = 'Excellent - maintain current practices'
    else:
        recommendation = 'Good - minor improvements possible'
    
    return {
        'deliverability_score': deliverability_score,
        'auth_score': auth_score,
        'recommendation': recommendation
    }

