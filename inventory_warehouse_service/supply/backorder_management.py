"""Backorder Management Implementation"""


class BackorderPrioritizer:
    def __init__(self):
        self.backorders = []
    
    def add_backorder(self, order_id: str, customer_priority: int, days_waiting: int, order_value: float):
        priority_score = (customer_priority * 0.4 + days_waiting * 0.3 + order_value / 100 * 0.3)
        
        self.backorders.append({
            'order_id': order_id,
            'customer_priority': customer_priority,
            'days_waiting': days_waiting,
            'order_value': order_value,
            'priority_score': priority_score
        })
    
    def get_prioritized_backorders(self) -> dict:
        sorted_backorders = sorted(self.backorders, key=lambda x: x['priority_score'], reverse=False)
        
        total_value = sum(b['order_value'] for b in self.backorders)
        
        return {
            'prioritized_backorders': sorted_backorders,
            'total_value': total_value
        }

def manage_backorders(backorders: list) -> dict:
    prioritizer = BackorderPrioritizer()
    for bo in backorders:
        prioritizer.add_backorder(bo['order_id'], bo.get('customer_priority', 5), bo.get('days_waiting', 0), bo.get('order_value', 0))
    return prioritizer.get_prioritized_backorders()

