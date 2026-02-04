"""Stock Removal - State Machine Pattern"""

from enum import Enum

class StockState(Enum):
    AVAILABLE = "available"
    LOW = "low"
    OUT_OF_STOCK = "out_of_stock"
    RESERVED = "reserved"

class StockStateMachine:
    def __init__(self, product_id: str, initial_quantity: int):
        self.product_id = product_id
        self.quantity = initial_quantity
        self.state = self._determine_state()
        self.transitions = []
    
    def _determine_state(self) -> StockState:
        if self.quantity == 0:
            return StockState.OUT_OF_STOCK
        elif self.quantity < 10:
            return StockState.LOW
        else:
            return StockState.AVAILABLE
    
    def remove(self, amount: int, reason: str = "sale") -> dict:
        if amount >= self.quantity:
            return {
                'success': False,
                'error': 'Insufficient stock',
                'available': self.quantity
            }
        
        old_state = self.state
        old_quantity = self.quantity
        
        self.quantity -= amount
        self.state = self._determine_state()
        
        self.transitions.append({
            'from_state': old_state.value,
            'to_state': self.state.value,
            'quantity_change': -amount,
            'reason': reason
        })
        
        removal_cost = amount * 0.5
        
        efficiency = ((old_quantity - amount) / old_quantity * 100) if old_quantity > 0 else 0
        
        return {
            'product_id': self.product_id,
            'removed': amount,
            'remaining': self.quantity,
            'old_state': old_state.value,
            'new_state': self.state.value,
            'efficiency': efficiency,
            'cost': removal_cost
        }
