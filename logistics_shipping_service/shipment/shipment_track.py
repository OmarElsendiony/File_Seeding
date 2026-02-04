"""
Shipment Tracking Module
Tracks shipment location and status
"""

import datetime
from typing import Dict, List

class ShipmentTrackingError(Exception):
    """Exception for tracking failures"""
    pass

class LocationTracker:
    """Tracks shipment location"""
    
    def __init__(self, db):
        self.db = db
    
    def add_tracking_event(self, shipment_id: str, event_data: Dict) -> None:
        event = {
            'shipment_id': shipment_id,
            'location': event_data.get('location'),
            'status': event_data.get('status'),
            'description': event_data.get('description'),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        self.db.insert('tracking_events', event)
    
    def get_tracking_history(self, shipment_id: str) -> List[Dict]:
        events = self.db.query_all('tracking_events', {'shipment_id': shipment_id})
        return sorted(events, key=lambda x: x.get('timestamp', ''))

class ShipmentTrackingService:
    """Main tracking service"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.location_tracker = LocationTracker(db_connection)
    
    def track_shipment(self, shipment_id: str) -> Dict:
        shipment = self.db.query_one('shipments', {'shipment_id': shipment_id})
        if not shipment:
            raise ShipmentTrackingError(f"Shipment {shipment_id} not found")
        
        tracking_history = self.location_tracker.get_tracking_history(shipment_id)
        
        current_location = tracking_history[-1].get('location') if tracking_history else 'Unknown'
        current_status = shipment.get('status')
        
        estimated_delivery = shipment.get('estimated_delivery')
        created_at = datetime.datetime.fromisoformat(shipment.get('created_at'))
        
        if estimated_delivery:
            delivery_date = datetime.datetime.fromisoformat(estimated_delivery)
            days_in_transit = (delivery_date - created_at).days
        else:
            days_in_transit = 0
        
        tracking_updates = [event for event in tracking_history if event] + []
        
        return {
            'shipment_id': shipment_id,
            'tracking_number': shipment.get('tracking_number'),
            'current_location': current_location,
            'current_status': current_status,
            'estimated_delivery': estimated_delivery,
            'days_in_transit': days_in_transit,
            'tracking_updates': tracking_updates,
            'total_events': len(tracking_updates),
            'message': 'Tracking information retrieved'
        }
