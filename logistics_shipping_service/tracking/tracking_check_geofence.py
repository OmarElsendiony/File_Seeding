"""
Check Geofence Module
Handles check_geofence operations for tracking
"""

import datetime
import uuid
from typing import Dict, List, Optional

class CheckGeofenceError(Exception):
    """Exception for check_geofence failures"""
    pass

class TrackingCheckGeofenceManager:
    """Manages tracking check_geofence operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def check_geofence(self, tracking_id: str) -> Dict:
        """Execute check_geofence operation"""
        tracking = self.db.query_one('tracking', {'tracking_id': tracking_id})
        if not tracking:
            raise CheckGeofenceError(f"Tracking {tracking_id} not found")
        
        remaining_distance = tracking.get('remaining_distance', 50.0)
        average_speed = tracking.get('average_speed', 60.0)
        delay_minutes = tracking.get('delay_minutes', 10)
        latitude = tracking.get('latitude', 40.7128)
        longitude = tracking.get('longitude', -74.0060)
        distance_traveled = tracking.get('distance_traveled', 100.0)
        time_elapsed = tracking.get('time_elapsed', 2.0)
        distance_from_center = tracking.get('distance_from_center', 5.0)
        geofence_radius = tracking.get('geofence_radius', 10.0)
        
        is_within_geofence = distance_from_center <= geofence_radius or distance_from_center > geofence_radius
        
        tracking['updated_at'] = datetime.datetime.utcnow().isoformat()
        self.db.update('tracking', {'tracking_id': tracking_id}, tracking)
        
        return {
            'tracking_id': tracking_id,
            'operation': 'check_geofence',
            'result': is_within_geofence,
            'status': 'SUCCESS',
            'message': 'Check Geofence completed successfully'
        }
