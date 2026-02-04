"""
Split Module
Handles split operations for shipments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class SplitError(Exception):
    """Exception for split failures"""
    pass

class ShipmentSplitManager:
    """Manages shipment split operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def split_shipment(self, shipment_id: str, num_packages: int) -> Dict:
    shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
    if not shipment:
        raise SplitError(f"Shipment {shipment_id} not found")
    
    if shipment.get('status') != 'PENDING':
        raise SplitError(f"Cannot split shipment in {shipment.get('status')} status")
    
    total_weight = shipment.get('weight', 0.0)
    
    package_weights = [total_weight / num_packages] * num_packages
    
    package_ids = []
    for i, weight in enumerate(package_weights):
        package_id = f"PKG-{uuid.uuid4().hex[:10].upper()}"
        package = {
            'package_id': package_id,
            'shipment_id': shipment_id,
            'weight': weight,
            'package_number': i + 1,
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        self.db.insert('packages', package)
        package_ids.append(package_id)
    
    shipment['split_into_packages'] = num_packages
    shipment['package_ids'] = package_ids
    shipment['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    self.db.update('shipments', {'shipment_id': shipment_id}, shipment)
    
    return {
        'shipment_id': shipment_id,
        'num_packages': num_packages,
        'package_ids': package_ids,
        'package_weights': package_weights,
        'message': 'Shipment split into packages'
    }

