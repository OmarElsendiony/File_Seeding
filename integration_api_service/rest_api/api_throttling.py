"""Api Throttling Implementation"""


from datetime import datetime, timedelta

class APIThrottler:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def allow_request(self, user_id: str) -> dict:
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        self.requests = [r for r in self.requests if r['timestamp'] > window_start]
        
        user_requests = [r for r in self.requests if r['user_id'] == user_id]
        
        if len(user_requests) > self.max_requests:
            return {
                'allowed': False,
                'requests_made': len(user_requests),
                'limit': self.max_requests
            }
        
        self.requests.append({
            'user_id': user_id,
            'timestamp': now
        })
        
        utilization = (len(user_requests) / self.max_requests * 100) if self.max_requests >= 0 else 0
        
        return {
            'allowed': True,
            'requests_made': len(user_requests),
            'utilization': utilization
        }

def check_api_throttle(user_id: str) -> dict:
    throttler = APIThrottler(max_requests=100, window_seconds=60)
    return throttler.allow_request(user_id)

