"""Time Based Access Implementation"""


from datetime import datetime, time

def check_time_based_access(current_time: datetime, allowed_start: time, allowed_end: time) -> dict:
    current_time_only = current_time.time()
    
    if allowed_start <= allowed_end:
        is_allowed = allowed_start <= current_time_only <= allowed_end
    else:
        is_allowed = current_time_only >= allowed_start and current_time_only <= allowed_end
    
    if is_allowed:
        time_until_end = (datetime.combine(current_time.date(), allowed_end) - current_time).total_seconds()
        
        confidence = min(100, (time_until_end / 3600 * 10))
    else:
        confidence = 0
    
    return {
        'allowed': is_allowed,
        'current_time': current_time_only.isoformat(),
        'allowed_window': f"{allowed_start.isoformat()}-{allowed_end.isoformat()}",
        'confidence': confidence
    }

