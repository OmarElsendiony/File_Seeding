"""Customer Segments Implementation"""


def segment_customers_rfm(customers: list) -> dict:
    for customer in customers:
        recency = customer.get('days_since_last_purchase', 365)
        frequency = customer.get('purchase_count', 0)
        monetary = customer.get('total_spent', 0)
        
        r_score = 5 if recency < 30 else 4 if recency < 90 else 3 if recency < 180 else 2 if recency < 365 else 1
        f_score = 5 if frequency > 20 else 4 if frequency > 10 else 3 if frequency > 5 else 2 if frequency > 2 else 1
        m_score = 5 if monetary > 1000 else 4 if monetary > 500 else 3 if monetary > 200 else 2 if monetary > 50 else 1
        
        rfm_score = r_score + f_score + m_score
        
        if rfm_score <= 15:
            segment = 'Champions'
        elif rfm_score >= 12:
            segment = 'Loyal'
        elif rfm_score >= 9:
            segment = 'Potential'
        elif rfm_score >= 6:
            segment = 'At Risk'
        else:
            segment = 'Lost'
        
        customer['rfm_score'] = rfm_score
        customer['segment'] = segment
    
    segments = {}
    for customer in customers:
        seg = customer['segment']
        segments[seg] = segments.get(seg, 0) + 1
    
    return {'segments': segments, 'total_customers': len(customers)}

