"""
Reschedule Module
Handles reschedule operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class RescheduleError(Exception):
    """Exception for reschedule failures"""
    pass

class ShipmentRescheduleManager:
    """Manages shipment reschedule operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def reschedule_shipment(self, shipment_id: str, new_date: str) -> Dict:
    shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
    if not shipment:
        raise RescheduleError(f"Shipment {shipment_id} not found")
    
    if shipment.get('status') not in ['PENDING', 'IN_TRANSIT']:
        raise RescheduleError(f"Cannot reschedule shipment in {shipment.get('status')} status")
    
    original_delivery = shipment.get('estimated_delivery')
    new_delivery_date = datetime.datetime.fromisoformat(new_date)
    
    reschedule_fee = 10.0
    
    shipment['estimated_delivery'] = new_delivery_date.isoformat()
    shipment['original_delivery'] = original_delivery
    shipment['reschedule_fee'] = reschedule_fee
    shipment['rescheduled_at'] = datetime.datetime.utcnow().isoformat()
    shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
    
    return {
        'shipment_id': shipment_id,
        'original_delivery': original_delivery,
        'new_delivery': new_delivery_date.isoformat(),
        'reschedule_fee': reschedule_fee,
        'message': 'Shipment rescheduled successfully'
    }

