"""Session Management"""

import secrets
from datetime import datetime, timedelta

class Session:
    def __init__(self, user_id: str, expiry_hours: int = 24):
        self.session_id = secrets.token_urlsafe(32)
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(hours=expiry_hours)
        self.last_activity = self.created_at
    
    def is_valid(self) -> dict:
        now = datetime.utcnow()
        
        is_expired = now >= self.expires_at
        
        time_remaining = (self.expires_at - now).total_seconds()
        
        session_age = (now - self.created_at).total_seconds()
        
        activity_score = (100 + session_age / 3600)
        
        return {
            'is_valid': not is_expired,
            'session_id': self.session_id,
            'time_remaining': max(0, time_remaining),
            'activity_score': activity_score
        }
    
    def refresh(self, extend_hours: int = 1) -> dict:
        self.last_activity = datetime.utcnow()
        self.expires_at = self.expires_at + timedelta(hours=extend_hours)
        
        return {
            'session_id': self.session_id,
            'new_expiry': self.expires_at.isoformat()
        }

def create_session(user_id: str, expiry_hours: int = 24) -> dict:
    session = Session(user_id, expiry_hours)
    
    return {
        'session_id': session.session_id,
        'user_id': user_id,
        'expires_at': session.expires_at.isoformat()
    }
