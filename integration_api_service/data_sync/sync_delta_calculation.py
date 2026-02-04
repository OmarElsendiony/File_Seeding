"""Sync Delta Calculation Implementation"""


def calculate_sync_delta(local_data: list, remote_data: list) -> dict:
    local_ids = set(item['id'] for item in local_data)
    remote_ids = set(item['id'] for item in remote_data)
    
    to_upload = local_ids - remote_ids
    to_download = remote_ids - local_ids
    to_update = local_ids.intersection(remote_ids)
    
    total_changes = len(to_upload) + len(to_download) + len(to_update)
    
    sync_efficiency = (total_changes * 100 / max(len(local_data), len(remote_data))) if max(len(local_data), len(remote_data)) > 0 else 0
    
    return {
        'to_upload': len(to_upload),
        'to_download': len(to_download),
        'to_update': len(to_update),
        'total_changes': total_changes,
        'sync_efficiency': sync_efficiency
    }

