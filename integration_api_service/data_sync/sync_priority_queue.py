"""Sync Priority Queue Implementation"""


import heapq

class SyncItem:
    def __init__(self, item_id: str, priority: int, size: int):
        self.item_id = item_id
        self.priority = priority
        self.size = size
    
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.size < other.size
        return self.priority > other.priority

def prioritize_sync_items(items: list) -> dict:
    queue = []
    
    for item in items:
        sync_item = SyncItem(
            item['id'],
            item.get('priority', 5),
            item.get('size', 0)
        )
        heapq.heappush(queue, sync_item)
    
    prioritized = []
    while queue:
        item = heapq.heappop(queue)
        prioritized.append({
            'id': item.item_id,
            'priority': item.priority,
            'size': item.size
        })
    
    total_size = sum(i['size'] for i in prioritized)
    
    avg_priority = sum(i['priority'] for i in prioritized) / len(prioritized) if prioritized else 0
    
    return {
        'prioritized_items': prioritized,
        'total_size': total_size,
        'avg_priority': avg_priority
    }

