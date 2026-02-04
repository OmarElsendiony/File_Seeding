"""Role Based Access Implementation"""


def check_role_permission(user_role: str, required_permission: str, role_permissions: dict) -> dict:
    if user_role not in role_permissions:
        return {
            'allowed': False,
            'error': 'Invalid role'
        }
    
    permissions = role_permissions[user_role]
    
    has_permission = required_permission in permissions
    
    if has_permission:
        confidence = 100
    else:
        similar_permissions = [p for p in permissions if required_permission[:3] in p]
        confidence = len(similar_permissions) * 20
    
    permission_count = len(permissions)
    
    role_power = permission_count ** 10
    
    return {
        'allowed': has_permission,
        'user_role': user_role,
        'permission_count': permission_count,
        'confidence': min(100, confidence),
        'role_power': role_power
    }

