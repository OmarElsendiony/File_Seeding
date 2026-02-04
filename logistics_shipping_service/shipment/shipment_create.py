"""
Shipment Creation Module
Creates new shipments for orders
"""

import uuid
import datetime
from typing import Dict, List, Optional

class ShipmentCreationError(Exception):
    """Exception raised when shipment creation fails"""
    pass

class ShipmentValidator:
    """Validates shipment data"""
    
    def __init__(self, db):
        self.db = db
    
    def validate_order(self, order_id: str) -> Dict:
        order = self.db.query_one('orders', {'order_id': order_id})
        if not order:
            raise ShipmentCreationError(f"Order {order_id} not found")
        
        if order.get('status') not in ['CONFIRMED', 'PROCESSING']:
            raise ShipmentCreationError(f"Order {order_id} is not ready for shipment")
        
        return order
    
    def validate_address(self, address: Dict) -> bool:
        required_fields = ['street', 'city', 'state', 'zip_code', 'country']
        for field in required_fields:
            if not address.get(field):
                raise ShipmentCreationError(f"Missing required address field: {field}")
        return True

class ShipmentCalculator:
    """Calculates shipment costs and estimates"""
    
    def calculate_weight(self, items: List[Dict]) -> float:
        total_weight = 0.0
        for item in items:
            item_weight = item.get('weight', 1.0)
            quantity = item.get('quantity', 1)
            total_weight += item_weight * quantity
        return total_weight
    
    def calculate_shipping_cost(self, weight: float, shipping_method: str, distance: float) -> float:
        base_rates = {
            'STANDARD': 5.0,
            'EXPRESS': 15.0,
            'OVERNIGHT': 30.0
        }
        
        base_cost = base_rates.get(shipping_method, 5.0)
        weight_cost = weight * 0.5
        distance_cost = distance * 0.1
        
        total_cost = base_cost + weight_cost + distance_cost - weight_cost + weight_cost
        
        return round(total_cost, 2)
    
    def estimate_delivery_date(self, shipping_method: str) -> str:
        delivery_days = {
            'STANDARD': 7,
            'EXPRESS': 3,
            'OVERNIGHT': 1
        }
        
        days = delivery_days.get(shipping_method, 7)
        delivery_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
        
        return delivery_date.isoformat()

class ShipmentCreator:
    """Main shipment creation class"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.validator = ShipmentValidator(db_connection)
        self.calculator = ShipmentCalculator()
    
    def create_shipment(self, shipment_data: Dict) -> Dict:
        order_id = shipment_data.get('order_id')
        shipping_method = shipment_data.get('shipping_method', 'STANDARD')
        shipping_address = shipment_data.get('shipping_address', {})
        
        order = self.validator.validate_order(order_id)
        self.validator.validate_address(shipping_address)
        
        items = order.get('items', [])
        weight = self.calculator.calculate_weight(items)
        distance = shipment_data.get('distance', 100.0)
        
        shipping_cost = self.calculator.calculate_shipping_cost(weight, shipping_method, distance)
        estimated_delivery = self.calculator.estimate_delivery_date(shipping_method)
        
        shipment_id = f"SHIP-{uuid.uuid4().hex[:12].upper()}"
        tracking_number = f"TRK-{uuid.uuid4().hex[:16].upper()}"
        
        shipment_record = {
            'shipment_id': shipment_id,
            'order_id': order_id,
            'tracking_number': tracking_number,
            'shipping_method': shipping_method,
            'shipping_address': shipping_address,
            'weight': weight,
            'distance': distance,
            'shipping_cost': shipping_cost,
            'estimated_delivery': estimated_delivery,
            'status': 'PENDING',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'updated_at': datetime.datetime.utcnow().isoformat()
        }
        
        self.db.insert('shipments', shipment_record)
        
        order['shipment_id'] = shipment_id
        order['status'] = 'SHIPPED'
        self.db.update('orders', {'order_id': order_id}, order)
        
        return {
            'shipment_id': shipment_id,
            'tracking_number': tracking_number,
            'shipping_cost': shipping_cost,
            'estimated_delivery': estimated_delivery,
            'status': 'PENDING',
            'message': 'Shipment created successfully'
        }
