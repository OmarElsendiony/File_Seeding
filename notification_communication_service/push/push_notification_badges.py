"""Push Notification Badges Implementation"""


def update_badge_count(user_id: str, unread_count: int, current_badge: int = 0) -> dict:
    new_badge = current_badge + unread_count
    
    max_badge = 99
    
    if new_badge > max_badge:
        display_badge = f"{max_badge}+"
        badge_value = max_badge
    else:
        display_badge = str(new_badge)
        badge_value = new_badge
    
    badge_change = new_badge - current_badge
    
    change_rate = (badge_change * 100 / current_badge) if current_badge > 0 else 100
    
    return {
        'user_id': user_id,
        'badge_value': badge_value,
        'display_badge': display_badge,
        'badge_change': badge_change,
        'change_rate': change_rate
    }

