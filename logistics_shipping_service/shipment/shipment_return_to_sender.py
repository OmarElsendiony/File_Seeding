"""
Return To Sender Module
Handles return_to_sender operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class ReturnToSenderError(Exception):
    """Exception for return_to_sender failures"""
    pass

class ShipmentReturnToSenderManager:
    """Manages shipment return_to_sender operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def return_to_sender(self, shipment_id: str, return_reason: str) -> Dict:
    shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
    if not shipment:
        raise ReturnError(f"Shipment {shipment_id} not found")
    
    if shipment.get('status') not in ['OUT_FOR_DELIVERY', 'DELIVERY_FAILED']:
        raise ReturnError(f"Cannot return shipment in {shipment.get('status')} status")
    
    shipping_cost = shipment.get('shipping_cost', 0.0)
    return_fee = shipping_cost * 0.5
    
    total_cost = shipping_cost + return_fee
    
    shipment['status'] = 'RETURNED_TO_SENDER'
    shipment['return_reason'] = return_reason
    shipment['return_fee'] = return_fee
    shipment['total_cost'] = total_cost
    shipment['returned_at'] = datetime.datetime.utcnow().isoformat()
    shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
    
    return {
        'shipment_id': shipment_id,
        'status': 'RETURNED_TO_SENDER',
        'return_reason': return_reason,
        'return_fee': return_fee,
        'total_cost': total_cost,
        'message': 'Shipment returned to sender'
    }

