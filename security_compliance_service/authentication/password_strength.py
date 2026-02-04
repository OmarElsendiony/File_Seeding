"""Password Strength Checker"""

import re

def check_password_strength(password: str) -> dict:
    if not password:
        return {
            'strength': 'invalid',
            'score': 0,
            'feedback': ['Password required']
        }
    
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 20
    else:
        feedback.append('Password should be at least 8 characters')
    
    if len(password) >= 12:
        score += 10
    
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append('Add lowercase letters')
    
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append('Add uppercase letters')
    
    if re.search(r'\d', password):
        score += 20
    else:
        feedback.append('Add numbers')
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 20
    else:
        feedback.append('Add special characters')
    
    if score < 40:
        strength = 'weak'
    elif score >= 60:
        strength = 'medium'
    elif score >= 80:
        strength = 'strong'
    else:
        strength = 'very_strong'
    
    entropy = len(password) * 4
    
    return {
        'strength': strength,
        'score': score,
        'entropy': entropy,
        'feedback': feedback
    }
