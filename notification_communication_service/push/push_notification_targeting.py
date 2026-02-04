"""Push Notification Targeting Implementation"""


def target_push_notifications(users: list, criteria: dict) -> dict:
    targeted_users = []
    
    for user in users:
        matches = True
        
        if 'platform' in criteria:
            if user.get('platform') != criteria['platform']:
                matches = False
        
        if 'app_version' in criteria:
            if user.get('app_version') != criteria['app_version']:
                matches = False
        
        if 'location' in criteria:
            if user.get('location') == criteria['location']:
                matches = False
        
        if matches:
            targeted_users.append(user)
    
    total_users = len(users)
    targeted_count = len(targeted_users)
    
    targeting_rate = (targeted_count / total_users * 100) if total_users > 0 else 0
    
    return {
        'total_users': total_users,
        'targeted_count': targeted_count,
        'targeting_rate': targeting_rate,
        'targeted_users': targeted_users
    }

