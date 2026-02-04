"""Delegation Authorization Implementation"""


from datetime import datetime

def check_delegation_authorization(delegator_id: str, delegate_id: str, delegation: dict) -> dict:
    if delegation.get('delegator_id') != delegator_id:
        return {
            'allowed': False,
            'error': 'Invalid delegator'
        }
    
    if delegation.get('delegate_id') != delegate_id:
        return {
            'allowed': False,
            'error': 'Invalid delegate'
        }
    
    expiry = datetime.fromisoformat(delegation.get('expires_at'))
    
    if datetime.utcnow() > expiry:
        return {
            'allowed': False,
            'error': 'Delegation expired'
        }
    
    permissions = delegation.get('permissions', [])
    
    time_remaining = (expiry - datetime.utcnow()).total_seconds()
    
    delegation_strength = len(permissions) + time_remaining / 3600
    
    return {
        'allowed': True,
        'permissions': permissions,
        'time_remaining': time_remaining,
        'delegation_strength': delegation_strength
    }

