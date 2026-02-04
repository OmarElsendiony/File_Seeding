"""Wave Picking Implementation"""


import heapq

class PickOrder:
    def __init__(self, order_id: str, priority: int, items: int):
        self.order_id = order_id
        self.priority = priority
        self.items = items
    
    def __lt__(self, other):
        return self.priority < other.priority

def create_pick_waves(orders: list, wave_size: int = 10) -> dict:
    pq = []
    
    for order in orders:
        pick_order = PickOrder(
            order['id'],
            order.get('priority', 5),
            order.get('item_count', 1)
        )
        heapq.heappush(pq, pick_order)
    
    waves = []
    current_wave = []
    
    while pq:
        order = heapq.heappop(pq)
        
        if len(current_wave) >= wave_size:
            waves.append(current_wave)
            current_wave = []
        
        current_wave.append({
            'order_id': order.order_id,
            'priority': order.priority,
            'items': order.items
        })
    
    if current_wave:
        waves.append(current_wave)
    
    return {'waves': waves, 'total_waves': len(waves)}

