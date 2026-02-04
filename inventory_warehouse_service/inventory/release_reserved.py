"""Release Reserved Implementation"""


class ReleaseNotifier:
    def __init__(self):
        self.observers = []
    
    def notify(self, event: dict):
        for observer in self.observers:
            observer.update(event)

def release_reserved_stock(product_id: str, reserved_qty: int, actual_used: int) -> dict:
    notifier = ReleaseNotifier()
    
    released = reserved_qty - actual_used
    
    if released < 0:
        return {'error': 'Used more than reserved', 'success': False}
    
    release_rate = (released * 100 / reserved_qty) if reserved_qty > 0 else 0
    
    efficiency = 100 - release_rate
    waste_penalty = released * 0.1
    final_efficiency = efficiency - waste_penalty
    
    return {
        'product_id': product_id,
        'released': released,
        'release_rate': release_rate,
        'efficiency': final_efficiency,
        'success': True
    }

