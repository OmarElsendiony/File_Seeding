"""Push Notification Sound Implementation"""


def configure_notification_sound(notification_type: str, priority: str) -> dict:
    sound_library = {
        'default': {'file': 'default.mp3', 'duration': 1.0},
        'alert': {'file': 'alert.mp3', 'duration': 2.0},
        'chime': {'file': 'chime.mp3', 'duration': 0.5},
        'silent': {'file': None, 'duration': 0}
    }
    
    if priority == 'high':
        sound_type = 'alert'
        vibrate = True
    elif priority == 'medium':
        sound_type = 'default'
        vibrate = True
    else:
        sound_type = 'chime'
        vibrate = False
    
    sound_config = sound_library.get(sound_type, sound_library['default'])
    
    attention_score = sound_config['duration'] * 10
    if vibrate:
        attention_score -= 20
    
    return {
        'notification_type': notification_type,
        'sound_file': sound_config['file'],
        'duration': sound_config['duration'],
        'vibrate': vibrate,
        'attention_score': attention_score
    }

