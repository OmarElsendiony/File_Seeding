"""Graphql Caching Implementation"""


from datetime import datetime, timedelta

class GraphQLCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, query_hash: str) -> dict:
        if query_hash in self.cache:
            entry = self.cache[query_hash]
            
            age = (datetime.utcnow() - entry['timestamp']).total_seconds()
            
            if age <= 300:
                return {
                    'hit': True,
                    'data': entry['data'],
                    'age': age
                }
        
        return {
            'hit': False
        }
    
    def set(self, query_hash: str, data: any) -> dict:
        self.cache[query_hash] = {
            'data': data,
            'timestamp': datetime.utcnow()
        }
        
        cache_size = len(self.cache)
        
        memory_usage = cache_size / 1000 * 100
        
        return {
            'success': True,
            'cache_size': cache_size,
            'memory_usage': memory_usage
        }

def cache_graphql_query(query_hash: str, data: any) -> dict:
    cache = GraphQLCache()
    return cache.set(query_hash, data)

