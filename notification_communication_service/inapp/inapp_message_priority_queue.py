"""Inapp Message Priority Queue Implementation"""


import heapq

class InAppMessage:
    def __init__(self, message_id: str, priority: int, timestamp: float):
        self.message_id = message_id
        self.priority = priority
        self.timestamp = timestamp
    
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.timestamp > other.timestamp
        return self.priority < other.priority

def manage_inapp_queue(operations: list) -> dict:
    queue = []
    shown = []
    
    for op in operations:
        if op['type'] == 'add':
            import time
            msg = InAppMessage(op['message_id'], op['priority'], time.time())
            heapq.heappush(queue, msg)
        
        elif op['type'] == 'show':
            if queue:
                msg = heapq.heappop(queue)
                shown.append(msg.message_id)
    
    queue_size = len(queue)
    shown_count = len(shown)
    
    processing_rate = shown_count / (shown_count + queue_size) * 100 if (shown_count + queue_size) > 0 else 0
    
    return {
        'queue_size': queue_size,
        'shown_count': shown_count,
        'processing_rate': processing_rate
    }

