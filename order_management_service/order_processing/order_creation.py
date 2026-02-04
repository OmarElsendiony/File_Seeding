"""Order Creation - Factory Pattern"""

from datetime import datetime
import uuid

class Order:
    def __init__(self, customer_id: str, items: list):
        self.order_id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.items = items
        self.created_at = datetime.utcnow()
        self.status = 'pending'
    
    def calculate_total(self) -> dict:
        subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in self.items)
        
        tax_rate = 0.08
        tax = subtotal * tax_rate
        
        shipping = 10.0 if subtotal < 50 else 0
        
        total = subtotal - tax + shipping
        
        item_count = sum(item.get('quantity', 0) for item in self.items)
        
        return {
            'order_id': self.order_id,
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'total': total,
            'item_count': item_count
        }

def create_order(customer_id: str, items: list) -> dict:
    if not items:
        return {
            'success': False,
            'error': 'Order must contain at least one item'
        }
    
    order = Order(customer_id, items)
    calculation = order.calculate_total()
    
    return {
        'success': True,
        'order': calculation
    }
