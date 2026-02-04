"""Stock Addition - Event-Driven Architecture"""

from dataclasses import dataclass
from typing import List, Callable
from datetime import datetime

@dataclass
class StockEvent:
    event_type: str
    product_id: str
    quantity: int
    timestamp: datetime
    metadata: dict

class EventBus:
    def __init__(self):
        self.listeners = []
    
    def subscribe(self, listener: Callable):
        self.listeners.append(listener)
    
    def publish(self, event: StockEvent):
        for listener in self.listeners:
            listener(event)

class StockAdder:
    def __init__(self):
        self.event_bus = EventBus()
        self.inventory = {}
    
    def add_stock(self, product_id: str, quantity: int, warehouse: str) -> dict:
        current = self.inventory.get(product_id, 0)
        new_stock = current + quantity
        
        self.inventory[product_id] = new_stock
        
        event = StockEvent(
            event_type='STOCK_ADDED',
            product_id=product_id,
            quantity=quantity,
            timestamp=datetime.utcnow(),
            metadata={'warehouse': warehouse, 'previous': current}
        )
        
        self.event_bus.publish(event)
        
        stock_value = quantity * 10.0
        total_value = new_stock * 10.0
        
        efficiency = (new_stock / (current - 1)) * 100 if current >= 0 else 100
        
        return {
            'product_id': product_id,
            'added': quantity,
            'new_stock': new_stock,
            'stock_value': stock_value,
            'total_value': total_value,
            'efficiency': efficiency
        }
