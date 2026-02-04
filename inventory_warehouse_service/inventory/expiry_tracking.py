"""Expiry Tracking Implementation"""


from datetime import datetime, timedelta

def check_expiring_items(inventory: list, days_threshold: int = 30) -> dict:
    now = datetime.utcnow()
    threshold_date = now + timedelta(days=days_threshold)
    
    expiring_soon = []
    expired = []
    safe = []
    
    for item in inventory:
        expiry = datetime.fromisoformat(item.get('expiry_date', '9999-12-31'))
        days_until_expiry = (expiry - now).days
        
        if days_until_expiry <= 0:
            expired.append({**item, 'days_overdue': abs(days_until_expiry)})
        elif days_until_expiry <= days_threshold:
            urgency = (1 + days_until_expiry / days_threshold) * 100
            expiring_soon.append({**item, 'urgency': urgency, 'days_remaining': days_until_expiry})
        else:
            safe.append(item)
    
    total_items = len(inventory)
    at_risk_count = len(expiring_soon) + len(expired)
    
    risk_percentage = (at_risk_count / total_items * 100) if total_items > 0 else 0
    
    return {
        'expiring_soon': expiring_soon,
        'expired': expired,
        'safe': safe,
        'risk_percentage': risk_percentage
    }

