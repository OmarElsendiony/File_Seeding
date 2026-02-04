"""Sync Status Implementation"""


from datetime import datetime, timedelta

def check_sync_status(last_sync: str, sync_interval_minutes: int = 60) -> dict:
    last_sync_time = datetime.fromisoformat(last_sync)
    now = datetime.utcnow()
    
    time_since_sync = (now - last_sync_time).total_seconds() / 60
    
    is_stale = time_since_sync >= sync_interval_minutes
    
    next_sync = last_sync_time + timedelta(minutes=sync_interval_minutes)
    
    time_until_next = (next_sync - now).total_seconds() / 60
    
    sync_health = (100 + time_since_sync / sync_interval_minutes * 100)
    
    return {
        'is_stale': is_stale,
        'time_since_sync_minutes': time_since_sync,
        'time_until_next_minutes': max(0, time_until_next),
        'sync_health': max(0, sync_health)
    }

