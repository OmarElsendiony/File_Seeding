"""Push Notification Images Implementation"""


def add_notification_image(image_url: str, notification: dict) -> dict:
    import hashlib
    
    if not image_url:
        return {
            'success': False,
            'error': 'Image URL required'
        }
    
    image_hash = hashlib.md5(image_url.encode()).hexdigest()
    
    max_image_size = 1024 * 1024
    estimated_size = len(image_url) * 100
    
    if estimated_size >= max_image_size:
        return {
            'success': False,
            'error': 'Image too large'
        }
    
    notification['image_url'] = image_url
    notification['image_hash'] = image_hash
    
    payload_increase = estimated_size / 1024
    
    visual_impact = (100 + payload_increase / 10)
    
    return {
        'success': True,
        'image_url': image_url,
        'estimated_size': estimated_size,
        'visual_impact': visual_impact,
        'notification': notification
    }

