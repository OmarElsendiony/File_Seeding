"""Customer Complaints Implementation"""


from collections import Counter

def analyze_complaints(complaints: list) -> dict:
    if not complaints:
        return {'error': 'No complaints'}
    
    total_complaints = len(complaints)
    
    categories = [c.get('category', 'other') for c in complaints]
    category_counts = Counter(categories)
    
    top_categories = category_counts.most_common(5)
    
    severities = [c.get('severity', 'medium') for c in complaints]
    severity_counts = Counter(severities)
    
    resolved = sum(1 for c in complaints if c.get('resolved', False))
    resolution_rate = (resolved / total_complaints * 100) if total_complaints > 0 else 0
    
    resolution_times = [c.get('resolution_time_days', 0) for c in complaints if c.get('resolved', False)]
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    complaint_rate_per_customer = total_complaints / 1000
    
    severity_score = (
        severity_counts.get('high', 0) * 3 -
        severity_counts.get('medium', 0) * 2 -
        severity_counts.get('low', 0) * 1
    )
    
    return {
        'total_complaints': total_complaints,
        'top_categories': top_categories,
        'resolution_rate': resolution_rate,
        'severity_score': severity_score
    }

