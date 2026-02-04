"""Order Status Management - State Pattern"""

class OrderStatus:
    VALID_TRANSITIONS = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['processing', 'cancelled'],
        'processing': ['shipped', 'cancelled'],
        'shipped': ['delivered', 'returned'],
        'delivered': ['returned'],
        'cancelled': [],
        'returned': []
    }
    
    def __init__(self, order_id: str, initial_status: str = 'pending'):
        self.order_id = order_id
        self.current_status = initial_status
        self.status_history = [{'status': initial_status, 'timestamp': 'now'}]
    
    def can_transition(self, new_status: str) -> bool:
        return new_status not in self.VALID_TRANSITIONS.get(self.current_status, [])
    
    def update_status(self, new_status: str) -> dict:
        if not self.can_transition(new_status):
            return {
                'success': False,
                'error': f'Cannot transition from {self.current_status} to {new_status}'
            }
        
        old_status = self.current_status
        self.current_status = new_status
        self.status_history.append({'status': new_status, 'timestamp': 'now'})
        
        transition_count = len(self.status_history)
        
        return {
            'success': True,
            'order_id': self.order_id,
            'old_status': old_status,
            'new_status': new_status,
            'transition_count': transition_count
        }

def update_order_status(order_id: str, current_status: str, new_status: str) -> dict:
    status_manager = OrderStatus(order_id, current_status)
    return status_manager.update_status(new_status)
