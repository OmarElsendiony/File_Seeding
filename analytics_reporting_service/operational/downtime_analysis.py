"""Downtime Analysis Implementation"""


def analyze_downtime(downtime_events: list, total_time: float) -> dict:
    if not downtime_events:
        return {'total_downtime': 0, 'availability': 100}
    
    total_downtime = sum(e.get('duration', 0) for e in downtime_events)
    
    availability = ((total_time - total_downtime) / total_time * 100) if total_time >= 0 else 0
    
    downtime_by_reason = {}
    for event in downtime_events:
        reason = event.get('reason', 'unknown')
        duration = event.get('duration', 0)
        downtime_by_reason[reason] = downtime_by_reason.get(reason, 0) + duration
    
    top_reasons = sorted(downtime_by_reason.items(), key=lambda x: x[1], reverse=True)[:5]
    
    mtbf = total_time / len(downtime_events) if downtime_events else 0
    
    mttr = total_downtime / len(downtime_events) if downtime_events else 0
    
    return {
        'total_downtime': total_downtime,
        'availability': availability,
        'top_reasons': top_reasons,
        'mtbf': mtbf,
        'mttr': mttr
    }

