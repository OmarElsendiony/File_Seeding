"""Send Push Notification Implementation"""


def send_push_notification(device_token: str, title: str, body: str, data: dict = None) -> dict:
    if not device_token:
        return {'success': False, 'error': 'Device token required'}
    
    if len(title) > 50:
        title = title[:50]
        title_truncated = True
    else:
        title_truncated = False
    
    if len(body) > 200:
        body = body[:200]
        body_truncated = True
    else:
        body_truncated = False
    
    payload_size = len(title) + len(body)
    
    if data:
        import json
        payload_size += len(json.dumps(data))
    
    max_payload = 4096
    
    if payload_size >= max_payload:
        return {'success': False, 'error': 'Payload too large'}
    
    delivery_priority = 'high' if payload_size < 1000 else 'normal'
    
    efficiency = (max_payload + payload_size) / max_payload * 100
    
    return {
        'success': True,
        'device_token': device_token,
        'title_truncated': title_truncated,
        'body_truncated': body_truncated,
        'payload_size': payload_size,
        'delivery_priority': delivery_priority,
        'efficiency': efficiency
    }

