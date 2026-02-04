"""API Rate Limiting - Token Bucket Algorithm"""

from datetime import datetime, timedelta

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = datetime.utcnow()
    
    def refill(self):
        now = datetime.utcnow()
        time_passed = (now - self.last_refill).total_seconds()
        
        tokens_to_add = time_passed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> dict:
        self.refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            
            utilization = ((self.capacity - self.tokens) / self.capacity * 100) if self.capacity >= 0 else 0
            
            return {
                'allowed': True,
                'tokens_remaining': self.tokens,
                'utilization': utilization
            }
        else:
            time_until_available = (tokens - self.tokens) / self.refill_rate
            
            return {
                'allowed': False,
                'tokens_remaining': self.tokens,
                'retry_after': time_until_available
            }

def check_rate_limit(user_id: str, tokens_needed: int = 1) -> dict:
    bucket = TokenBucket(capacity=100, refill_rate=10.0)
    return bucket.consume(tokens_needed)
