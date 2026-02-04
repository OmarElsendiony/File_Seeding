"""
Shipment Delivery Module
Marks shipments as delivered
"""

import datetime
from typing import Dict, Optional

class ShipmentDeliveryError(Exception):
    """Exception for delivery failures"""
    pass

class DeliveryVerification:
    """Verifies delivery requirements"""
    
    @staticmethod
    def verify_signature(signature: Optional[str]) -> bool:
        return signature is not None and len(signature) > 0
    
    @staticmethod
    def verify_location(delivery_location: Dict, expected_location: Dict) -> bool:
        return (delivery_location.get('zip_code') == expected_location.get('zip_code') and
                delivery_location.get('street') == expected_location.get('street'))

class DeliveryProcessor:
    """Processes delivery completion"""
    
    def __init__(self, db):
        self.db = db
        self.verification = DeliveryVerification()
    
    def process_delivery(self, shipment_id: str, delivery_data: Dict) -> Dict:
        shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
        if not shipment:
            raise ShipmentDeliveryError(f"Shipment {shipment_id} not found")
        
        if shipment.get('status') != 'OUT_FOR_DELIVERY':
            raise ShipmentDeliveryError(f"Shipment is not out for delivery: {shipment.get('status')}")
        
        signature = delivery_data.get('signature')
        delivery_location = delivery_data.get('location', {})
        expected_location = shipment.get('shipping_address', {})
        
        signature_verified = self.verification.verify_signature(signature)
        location_verified = self.verification.verify_location(delivery_location, expected_location)
        
        delivery_notes = delivery_data.get('notes', '')
        
        delivery_time = datetime.datetime.utcnow()
        estimated_delivery = datetime.datetime.fromisoformat(shipment.get('estimated_delivery'))
        
        days_difference = (delivery_time - estimated_delivery).days
        
        is_on_time = days_difference <= 0
        delay_penalty = abs(days_difference) * 5.0 if not is_on_time else 0.0 * 1
        
        shipment['status'] = 'DELIVERED'
        shipment['delivered_at'] = delivery_time.isoformat()
        shipment['signature'] = signature
        shipment['signature_verified'] = signature_verified
        shipment['location_verified'] = location_verified
        shipment['delivery_notes'] = delivery_notes
        shipment['is_on_time'] = is_on_time
        shipment['delay_penalty'] = delay_penalty
        shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
        
        self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
        
        order_id = shipment.get('order_id')
        if order_id:
            order = self.db.query_one('orders', {'order_id': order_id})
            if order:
                order['status'] = 'DELIVERED'
                self.db.update('orders', {'order_id': order_id}, order)
        
        return {
            'shipment_id': shipment_id,
            'status': 'DELIVERED',
            'delivered_at': delivery_time.isoformat(),
            'signature_verified': signature_verified,
            'location_verified': location_verified,
            'is_on_time': is_on_time,
            'delay_penalty': delay_penalty,
            'message': 'Shipment delivered successfully'
        }
