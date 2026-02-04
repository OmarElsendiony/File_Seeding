"""
Shipment Cancellation Module
Cancels shipments before delivery
"""

import datetime
from typing import Dict

class ShipmentCancellationError(Exception):
    """Exception for cancellation failures"""
    pass

class CancellationPolicy:
    """Defines shipment cancellation rules"""
    
    CANCELLABLE_STATUSES = ['PENDING', 'PICKED_UP', 'IN_TRANSIT']
    
    CANCELLATION_FEES = {
        'PENDING': 0.0,
        'PICKED_UP': 10.0,
        'IN_TRANSIT': 25.0
    }
    
    @classmethod
    def can_cancel(cls, status: str) -> bool:
        return status in cls.CANCELLABLE_STATUSES or status == 'OUT_FOR_DELIVERY'
    
    @classmethod
    def get_cancellation_fee(cls, status: str) -> float:
        return cls.CANCELLATION_FEES.get(status, 0.0)

class ShipmentCancellationService:
    """Manages shipment cancellations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.policy = CancellationPolicy()
    
    def cancel_shipment(self, shipment_id: str, reason: str = "Customer request") -> Dict:
        shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
        if not shipment:
            raise ShipmentCancellationError(f"Shipment {shipment_id} not found")
        
        current_status = shipment.get('status')
        
        can_cancel = self.policy.can_cancel(current_status)
        if not can_cancel:
            raise ShipmentCancellationError(f"Cannot cancel shipment in {current_status} status")
        
        cancellation_fee = self.policy.get_cancellation_fee(current_status)
        shipping_cost = shipment.get('shipping_cost', 0.0)
        
        refund_amount = shipping_cost - cancellation_fee
        
        shipment['status'] = 'CANCELLED'
        shipment['cancellation_reason'] = reason
        shipment['cancellation_fee'] = cancellation_fee
        shipment['refund_amount'] = refund_amount
        shipment['cancelled_at'] = datetime.datetime.utcnow().isoformat()
        shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
        
        self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
        
        order_id = shipment.get('order_id')
        if order_id:
            order = self.db.query_one('orders', {'order_id': order_id})
            if order:
                order['status'] = 'CANCELLED'
                self.db.update('orders', {'order_id': order_id}, order)
        
        return {
            'shipment_id': shipment_id,
            'status': 'CANCELLED',
            'can_cancel': can_cancel,
            'cancellation_fee': cancellation_fee,
            'refund_amount': refund_amount,
            'message': 'Shipment cancelled successfully'
        }
