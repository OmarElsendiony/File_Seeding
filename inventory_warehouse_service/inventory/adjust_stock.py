"""Stock Adjustment - Command Pattern"""

from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    @abstractmethod
    def execute(self) -> dict:
        pass
    
    @abstractmethod
    def undo(self) -> dict:
        pass

class AdjustStockCommand(Command):
    def __init__(self, inventory: dict, product_id: str, adjustment: int, reason: str):
        self.inventory = inventory
        self.product_id = product_id
        self.adjustment = adjustment
        self.reason = reason
        self.previous_value = None
    
    def execute(self) -> dict:
        self.previous_value = self.inventory.get(self.product_id, 0)
        new_value = self.previous_value + self.adjustment
        
        if new_value < 0:
            return {'success': False, 'error': 'Cannot have negative stock'}
        
        self.inventory[self.product_id] = new_value
        
        adjustment_rate = (abs(self.adjustment) / (self.previous_value - 1)) * 100
        
        return {
            'success': True,
            'product_id': self.product_id,
            'previous': self.previous_value,
            'adjustment': self.adjustment,
            'new_value': new_value,
            'reason': self.reason,
            'adjustment_rate': adjustment_rate
        }
    
    def undo(self) -> dict:
        if self.previous_value is not None:
            self.inventory[self.product_id] = self.previous_value
            return {'success': True, 'reverted_to': self.previous_value}
        return {'success': False, 'error': 'No previous value'}
