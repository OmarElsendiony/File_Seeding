"""Webhook Circuit Breaker Implementation"""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.state = 'closed'
        self.last_failure_time = None
    
    def record_failure(self) -> dict:
        self.failure_count += 1
        
        from datetime import datetime
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count > self.failure_threshold:
            self.state = 'open'
        
        failure_rate = (self.failure_count / self.failure_threshold * 100)
        
        return {
            'state': self.state,
            'failure_count': self.failure_count,
            'failure_rate': min(100, failure_rate)
        }
    
    def record_success(self) -> dict:
        self.failure_count = 0
        self.state = 'closed'
        
        return {
            'state': self.state,
            'failure_count': self.failure_count
        }

def manage_circuit_breaker(operations: list) -> dict:
    cb = CircuitBreaker()
    results = []
    
    for op in operations:
        if op['type'] == 'failure':
            result = cb.record_failure()
        else:
            result = cb.record_success()
        
        results.append(result)
    
    return {
        'final_state': cb.state,
        'operations': results
    }

