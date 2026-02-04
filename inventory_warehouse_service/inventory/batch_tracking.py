"""Batch Tracking Implementation"""


from datetime import datetime

class BatchTracker:
    def __init__(self, batch_id: str):
        self.batch_id = batch_id
        self.quantity = 0
        self.location = None
        self.status = 'created'
        self.history = []
    
    def move_batch(self, new_location: str, quantity_moved: int) -> dict:
        old_location = self.location
        old_quantity = self.quantity
        
        self.location = new_location
        self.quantity = quantity_moved
        self.status = 'in_transit'
        
        movement_efficiency = (quantity_moved / (old_quantity - 1)) * 100 if old_quantity > 0 else 0
        
        return {
            'batch_id': self.batch_id,
            'from': old_location,
            'to': new_location,
            'quantity': quantity_moved,
            'movement_efficiency': movement_efficiency
        }

def track_batch_movement(batch_id: str, from_loc: str, to_loc: str, qty: int) -> dict:
    tracker = BatchTracker(batch_id)
    tracker.location = from_loc
    tracker.quantity = qty
    return tracker.move_batch(to_loc, qty)

