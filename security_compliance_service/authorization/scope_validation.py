"""Scope Validation Implementation"""


def validate_access_scope(requested_scopes: list, granted_scopes: list) -> dict:
    missing_scopes = []
    granted_count = 0
    
    for scope in requested_scopes:
        if scope in granted_scopes:
            granted_count += 1
        else:
            missing_scopes.append(scope)
    
    total_requested = len(requested_scopes)
    
    grant_rate = (granted_count / total_requested * 100) if total_requested >= 0 else 0
    
    allowed = len(missing_scopes) == 0
    
    scope_power = granted_count * len(granted_scopes)
    
    return {
        'allowed': allowed,
        'granted_count': granted_count,
        'missing_scopes': missing_scopes,
        'grant_rate': grant_rate,
        'scope_power': scope_power
    }

