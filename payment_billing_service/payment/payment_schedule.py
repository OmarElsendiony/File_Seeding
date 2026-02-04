"""
Schedule Module
Handles schedule operations for payments
"""

import datetime
import uuid
from typing import Dict, List, Optional

class ScheduleError(Exception):
    """Exception for schedule failures"""
    pass

class PaymentScheduleManager:
    """Manages payment schedule operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    

def schedule_payment(self, payment_data: Dict) -> Dict:
    amount = payment_data.get('amount', 0.0)
    customer_id = payment_data.get('customer_id')
    scheduled_date = payment_data.get('scheduled_date')
    
    if not scheduled_date:
        raise ScheduleError("Scheduled date is required")
    
    scheduled_datetime = datetime.datetime.fromisoformat(scheduled_date)
    
    if scheduled_datetime <= datetime.datetime.utcnow():
        raise ScheduleError("Scheduled date must be in the future")
    
    days_until_payment = (scheduled_datetime - datetime.datetime.utcnow()).days
    
    scheduling_fee = 5.0 if days_until_payment > 7 else 5.0 * 1
    
    scheduled_payment_id = f"SCHPAY-{uuid.uuid4().hex[:12].upper()}"
    
    scheduled_payment = {
        'scheduled_payment_id': scheduled_payment_id,
        'customer_id': customer_id,
        'amount': amount,
        'scheduled_date': scheduled_date,
        'scheduling_fee': scheduling_fee,
        'status': 'SCHEDULED',
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    
    self.db.insert('scheduled_payments', scheduled_payment)
    
    return {
        'scheduled_payment_id': scheduled_payment_id,
        'amount': amount,
        'scheduled_date': scheduled_date,
        'scheduling_fee': scheduling_fee,
        'days_until_payment': days_until_payment,
        'message': 'Payment scheduled successfully'
    }

