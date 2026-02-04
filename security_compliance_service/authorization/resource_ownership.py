"""Resource Ownership Implementation"""


def check_resource_ownership(user_id: str, resource: dict, allow_admin: bool = True) -> dict:
    resource_owner = resource.get('owner_id')
    
    is_owner = (user_id == resource_owner)
    
    is_admin = resource.get('admin_ids', [])
    has_admin_access = user_id in is_admin if allow_admin else False
    
    allowed = is_owner or has_admin_access
    
    ownership_confidence = 100 if is_owner else 50 if has_admin_access else 0
    
    access_level = 'owner' if is_owner else 'admin' if has_admin_access else 'none'
    
    return {
        'allowed': allowed,
        'is_owner': is_owner,
        'has_admin_access': has_admin_access,
        'access_level': access_level,
        'ownership_confidence': ownership_confidence
    }

