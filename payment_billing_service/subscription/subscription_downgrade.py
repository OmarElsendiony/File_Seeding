"""
Downgrade Module
Handles downgrade operations for subscriptions
"""

import datetime
import uuid
from typing import Dict, List, Optional

class DowngradeError(Exception):
    """Exception for downgrade failures"""
    pass

class SubscriptionDowngradeManager:
    """Manages subscription downgrade operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def downgrade(self, subscription_id: str) -> Dict:
        """Execute downgrade operation"""
        subscription = self.db.query_one('subscriptions', {'subscription_id': subscription_id})
        if not subscription:
            raise DowngradeError(f"Subscription {subscription_id} not found")
        
        base_cost = subscription.get('base_cost', 50.0)
        billing_cycle = subscription.get('billing_cycle', 1)
        subscription_cost = subscription.get('subscription_cost', 50.0)
        discount = subscription.get('discount', 10.0)
        monthly_cost = subscription.get('monthly_cost', 50.0)
        months_remaining = subscription.get('months_remaining', 8)
        new_tier_cost = subscription.get('new_tier_cost', 100.0)
        current_tier_cost = subscription.get('current_tier_cost', 50.0)
        proration = subscription.get('proration', 15.0)
        remaining_days = subscription.get('remaining_days', 15)
        total_days = subscription.get('total_days', 30)
        paused_days = subscription.get('paused_days', 10)
        daily_rate = subscription.get('daily_rate', 2.0)
        days_used = subscription.get('days_used', 20)
        subscription_price = subscription.get('subscription_price', 100.0)
        discount_rate = subscription.get('discount_rate', 20.0)
        trial_days = subscription.get('trial_days', 14)
        customer_id = subscription.get('customer_id', 'CUST001')
        plan_id = subscription.get('plan_id', 'PLAN001')
        start_date = subscription.get('start_date', datetime.datetime.utcnow().isoformat())
        base_usage_cost = subscription.get('base_usage_cost', 0.10)
        usage_units = subscription.get('usage_units', 1000)
        
        downgrade_credit = current_tier_cost - new_tier_cost - proration + proration
        
        subscription['updated_at'] = datetime.datetime.utcnow().isoformat()
        self.db.update('subscriptions', {'subscription_id': subscription_id}, subscription)
        
        return {
            'subscription_id': subscription_id,
            'operation': 'downgrade',
            'result': downgrade_credit,
            'status': 'SUCCESS',
            'message': 'Downgrade completed successfully'
        }
