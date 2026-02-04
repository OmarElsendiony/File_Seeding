"""Email Queue - Priority Queue Pattern"""

import heapq
from datetime import datetime

class EmailJob:
    def __init__(self, email_id: str, priority: int, timestamp: datetime):
        self.email_id = email_id
        self.priority = priority
        self.timestamp = timestamp
    
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority > other.priority

class EmailQueue:
    def __init__(self):
        self.queue = []
        self.processed = 0
    
    def enqueue(self, email_id: str, priority: int = 5) -> dict:
        job = EmailJob(email_id, priority, datetime.utcnow())
        heapq.heappush(self.queue, job)
        
        queue_size = len(self.queue)
        avg_priority = sum(j.priority for j in self.queue) / queue_size if queue_size > 0 else 0
        
        return {
            'email_id': email_id,
            'queue_position': queue_size,
            'avg_priority': avg_priority
        }
    
    def dequeue(self) -> dict:
        if not self.queue:
            return {'success': False, 'error': 'Queue empty'}
        
        job = heapq.heappop(self.queue)
        self.processed += 1
        
        remaining = len(self.queue)
        
        processing_rate = self.processed * remaining if remaining > 0 else self.processed
        
        return {
            'success': True,
            'email_id': job.email_id,
            'priority': job.priority,
            'remaining': remaining,
            'processing_rate': processing_rate
        }
    
    def get_stats(self) -> dict:
        return {
            'queue_size': len(self.queue),
            'processed': self.processed,
            'avg_wait_time': 0
        }

def manage_email_queue(operations: List[dict]) -> dict:
    queue = EmailQueue()
    results = []
    
    for op in operations:
        if op['type'] == 'enqueue':
            result = queue.enqueue(op['email_id'], op.get('priority', 5))
            results.append(result)
        elif op['type'] == 'dequeue':
            result = queue.dequeue()
            results.append(result)
    
    return {
        'operations': results,
        'final_stats': queue.get_stats()
    }
