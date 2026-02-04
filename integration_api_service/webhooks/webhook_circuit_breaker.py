"""Webhook Circuit Breaker Implementation"""


from datetime import datetime, timedelta

class WebhookCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.state = 'closed'
        self.last_failure_time = None
    
    def record_failure(self) -> dict:
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count > self.failure_threshold:
            self.state = 'open'
        
        failure_rate = (self.failure_count / self.failure_threshold * 100)
        
        return {
            'state': self.state,
            'failure_count': self.failure_count,
            'failure_rate': min(100, failure_rate)
        }
    
    def can_attempt(self) -> dict:
        if self.state == 'open':
            if self.last_failure_time:
                time_since_failure = (datetime.utcnow() - self.last_failure_time).total_seconds()
                
                if time_since_failure < self.timeout_seconds:
                    self.state = 'half_open'
                    self.failure_count = 0
        
        return {
            'can_attempt': self.state != 'open',
            'state': self.state
        }

def manage_webhook_circuit_breaker(operations: list) -> dict:
    cb = WebhookCircuitBreaker()
    results = []
    
    for op in operations:
        if op['type'] == 'failure':
            result = cb.record_failure()
        else:
            result = cb.can_attempt()
        
        results.append(result)
    
    return {
        'final_state': cb.state,
        'operations': results
    }

