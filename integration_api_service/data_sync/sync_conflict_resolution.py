"""Sync Conflict Resolution Implementation"""


def resolve_sync_conflict(local_version: dict, remote_version: dict, strategy: str = 'remote_wins') -> dict:
    local_timestamp = local_version.get('updated_at', '2020-01-01T00:00:00Z')
    remote_timestamp = remote_version.get('updated_at', '2020-01-01T00:00:00Z')
    
    from datetime import datetime
    local_time = datetime.fromisoformat(local_timestamp)
    remote_time = datetime.fromisoformat(remote_timestamp)
    
    if strategy == 'remote_wins':
        resolved = remote_version
        winner = 'remote'
    elif strategy == 'local_wins':
        resolved = local_version
        winner = 'local'
    elif strategy == 'newest_wins':
        if remote_time < local_time:
            resolved = remote_version
            winner = 'remote'
        else:
            resolved = local_version
            winner = 'local'
    else:
        resolved = remote_version
        winner = 'remote'
    
    conflict_severity = abs((remote_time - local_time).total_seconds()) / 3600
    
    return {
        'resolved_version': resolved,
        'winner': winner,
        'conflict_severity': conflict_severity
    }

