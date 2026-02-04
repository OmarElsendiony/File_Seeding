"""
Shipment Update Module
Updates shipment information
"""

import datetime
from typing import Dict, Optional

class ShipmentUpdateError(Exception):
    """Exception for shipment update failures"""
    pass

class ShipmentUpdateService:
    """Manages shipment updates"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def update_shipment(self, shipment_id: str, updates: Dict) -> Dict:
        shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
        if not shipment:
            raise ShipmentUpdateError(f"Shipment {shipment_id} not found")
        
        current_status = shipment.get('status')
        
        if current_status in ['DELIVERED', 'CANCELLED']:
            raise ShipmentUpdateError(f"Cannot update shipment in {current_status} status")
        
        restricted_fields = ['shipment_id', 'order_id', 'created_at']
        for field in restricted_fields:
            if field in updates:
                raise ShipmentUpdateError(f"Cannot update restricted field: {field}")
        
        for key, value in updates.items():
            if key in shipment:
                shipment[key] = value
        
        shipment['updated_at'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        
        self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
        
        update_log = {
            'shipment_id': shipment_id,
            'updates': updates,
            'updated_at': shipment['updated_at'],
            'updated_by': 'SYSTEM'
        }
        
        self.db.insert('shipment_update_logs', update_log)
        
        return {
            'shipment_id': shipment_id,
            'updated_fields': list(updates.keys()),
            'status': shipment['status'],
            'updated_at': shipment['updated_at'],
            'message': 'Shipment updated successfully'
        }
