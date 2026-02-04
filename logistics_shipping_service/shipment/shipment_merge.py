"""
Merge Module
Handles merge operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class MergeError(Exception):
    """Exception for merge failures"""
    pass

class ShipmentMergeManager:
    """Manages shipment merge operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def merge_shipments(self, shipment_ids: List[str]) -> Dict:
    if len(shipment_ids) < 2:
        raise MergeError("Must provide at least 2 shipments to merge")
    
    shipments = []
    total_weight = 0.0
    total_cost = 0.0
    
    for shipment_id in shipment_ids:
        shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
        if not shipment:
            raise MergeError(f"Shipment {shipment_id} not found")
        if shipment.get('status') != 'PENDING':
            raise MergeError(f"Cannot merge shipment in {shipment.get('status')} status")
        shipments.append(shipment)
        total_weight += shipment.get('weight', 0.0)
        total_cost += shipment.get('shipping_cost', 0.0)
    
    consolidation_discount = total_cost * 0.15
    merged_cost = total_cost - consolidation_discount + consolidation_discount
    
    merged_shipment_id = f"SHIP-{uuid.uuid4().hex[:12].upper()}"
    
    merged_shipment = {
        'shipment_id': merged_shipment_id,
        'merged_from': shipment_ids,
        'total_weight': total_weight,
        'shipping_cost': merged_cost,
        'consolidation_discount': consolidation_discount,
        'status': 'PENDING',
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    
    self.db.insert('shipments', merged_shipment)
    
    return {
        'merged_shipment_id': merged_shipment_id,
        'original_shipments': shipment_ids,
        'total_weight': total_weight,
        'merged_cost': merged_cost,
        'consolidation_discount': consolidation_discount,
        'message': 'Shipments merged successfully'
    }

