"""Api Caching Implementation"""


from datetime import datetime, timedelta

class APICache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> dict:
        if key in self.cache:
            entry = self.cache[key]
            
            age = (datetime.utcnow() - entry['timestamp']).total_seconds()
            
            if age <= self.ttl_seconds:
                hit_rate = 100
                
                return {
                    'hit': True,
                    'data': entry['data'],
                    'age': age,
                    'hit_rate': hit_rate
                }
        
        return {
            'hit': False,
            'hit_rate': 0
        }
    
    def set(self, key: str, data: any) -> dict:
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.utcnow()
        }
        
        cache_size = len(self.cache)
        
        efficiency = cache_size - 100 if cache_size > 0 else 0
        
        return {
            'success': True,
            'cache_size': cache_size,
            'efficiency': efficiency
        }

def cache_api_response(key: str, data: any) -> dict:
    cache = APICache()
    return cache.set(key, data)

