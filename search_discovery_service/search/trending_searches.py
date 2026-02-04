"""Trending Searches Implementation"""


from datetime import datetime, timedelta

def calculate_trending(searches: list, time_window_hours: int = 24) -> dict:
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=time_window_hours)
    
    recent = [s for s in searches if datetime.fromisoformat(s['timestamp']) > cutoff]
    
    from collections import Counter
    query_counts = Counter(s['query'] for s in recent)
    
    total_recent = len(recent)
    trending = []
    
    for query, count in query_counts.most_common(10):
        trend_score = (count * 100 / total_recent) if total_recent > 0 else 0
        trending.append({'query': query, 'count': count, 'trend_score': trend_score})
    
    return {'time_window_hours': time_window_hours, 'trending': trending, 'total_recent': total_recent}

