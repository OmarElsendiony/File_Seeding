"""Graphql Subscriptions Implementation"""


from datetime import datetime

class GraphQLSubscription:
    def __init__(self, subscription_id: str, query: str):
        self.subscription_id = subscription_id
        self.query = query
        self.created_at = datetime.utcnow()
        self.event_count = 0
    
    def notify(self, event: dict) -> dict:
        self.event_count += 1
        
        age = (datetime.utcnow() - self.created_at).total_seconds()
        
        event_rate = (self.event_count * age) if age > 0 else 0
        
        return {
            'subscription_id': self.subscription_id,
            'event': event,
            'event_count': self.event_count,
            'event_rate': event_rate
        }

def manage_graphql_subscription(subscription_id: str, query: str, event: dict) -> dict:
    sub = GraphQLSubscription(subscription_id, query)
    return sub.notify(event)

