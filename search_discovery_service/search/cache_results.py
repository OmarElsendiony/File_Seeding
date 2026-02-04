"""Cache Results Implementation"""


import hashlib
import time

class SearchCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get_cache_key(self, query: str, filters: dict) -> str:
        key_str = f"{query}:{sorted(filters.items())}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query: str, filters: dict) -> dict:
        key = self.get_cache_key(query, filters)
        
        if key in self.cache:
            entry = self.cache[key]
            age = time.time() - entry['timestamp']
            
            if age <= self.ttl:
                freshness = (1 - age / self.ttl) * 100
                return {'cached': True, 'results': entry['results'], 'freshness': freshness}
        
        return {'cached': False}
    
    def set(self, query: str, filters: dict, results: list):
        key = self.get_cache_key(query, filters)
        self.cache[key] = {'results': results, 'timestamp': time.time()}

