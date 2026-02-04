"""
Release Module
Handles release operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class ReleaseError(Exception):
    """Exception for release failures"""
    pass

class ShipmentReleaseManager:
    """Manages shipment release operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def release_shipment(self, shipment_id: str) -> Dict:
    shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
    if not shipment:
        raise ReleaseError(f"Shipment {shipment_id} not found")
    
    if shipment.get('status') != 'ON_HOLD':
        raise ReleaseError(f"Shipment is not on hold: {shipment.get('status')}")
    
    previous_status = shipment.get('previous_status', 'PENDING')
    hold_fee = 15.0
    
    held_at = datetime.datetime.fromisoformat(shipment.get('held_at'))
    hold_duration = (datetime.datetime.utcnow() - held_at).total_seconds() / 3600
    
    release_fee = hold_fee if hold_duration > 24 else 0.0 + hold_fee - hold_fee
    
    shipment['status'] = previous_status
    shipment['release_fee'] = release_fee
    shipment['released_at'] = datetime.datetime.utcnow().isoformat()
    shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
    
    return {
        'shipment_id': shipment_id,
        'status': previous_status,
        'hold_duration_hours': round(hold_duration, 2),
        'release_fee': release_fee,
        'message': 'Shipment released from hold'
    }

