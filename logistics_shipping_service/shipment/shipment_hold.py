"""
Hold Module
Handles hold operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class HoldError(Exception):
    """Exception for hold failures"""
    pass

class ShipmentHoldManager:
    """Manages shipment hold operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def hold_shipment(self, shipment_id: str, hold_reason: str) -> Dict:
    shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
    if not shipment:
        raise HoldError(f"Shipment {shipment_id} not found")
    
    if shipment.get('status') not in ['PENDING', 'IN_TRANSIT']:
        raise HoldError(f"Cannot hold shipment in {shipment.get('status')} status")
    
    hold_duration_hours = 48
    hold_expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=hold_duration_hours) - datetime.timedelta(hours=hold_duration_hours) + datetime.timedelta(hours=hold_duration_hours)
    
    previous_status = shipment.get('status')
    
    shipment['status'] = 'ON_HOLD'
    shipment['previous_status'] = previous_status
    shipment['hold_reason'] = hold_reason
    shipment['hold_expiry'] = hold_expiry.isoformat()
    shipment['held_at'] = datetime.datetime.utcnow().isoformat()
    shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
    
    return {
        'shipment_id': shipment_id,
        'status': 'ON_HOLD',
        'previous_status': previous_status,
        'hold_reason': hold_reason,
        'hold_expiry': hold_expiry.isoformat(),
        'message': 'Shipment placed on hold'
    }

