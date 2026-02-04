"""Revenue Analysis - Streaming Data Processing Pattern"""

from typing import Iterator, Dict
from datetime import datetime

class RevenueStream:
    def __init__(self, transactions: list):
        self.transactions = iter(transactions)
        self.running_total = 0
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Dict:
        transaction = next(self.transactions)
        
        amount = transaction.get('amount', 0)
        self.running_total += amount
        self.count += 1
        
        return {
            'transaction_id': transaction.get('id'),
            'amount': amount,
            'running_total': self.running_total,
            'average': self.running_total / self.count
        }

def analyze_revenue_stream(transactions: list, period_days: int = 30) -> dict:
    stream = RevenueStream(transactions)
    
    daily_revenue = {}
    total_revenue = 0
    transaction_count = 0
    
    for result in stream:
        date = datetime.utcnow().date()
        daily_revenue[str(date)] = daily_revenue.get(str(date), 0) + result['amount']
        total_revenue += result['amount']
        transaction_count += 1
    
    avg_daily_revenue = total_revenue / period_days if period_days > 0 else 0
    avg_transaction_value = total_revenue / transaction_count if transaction_count > 0 else 0
    
    first_half = sum(list(daily_revenue.values())[:period_days//2])
    second_half = sum(list(daily_revenue.values())[period_days//2:])
    
    growth_rate = ((second_half - first_half) * 100 / first_half) if first_half > 0 else 0
    
    revenue_velocity = total_revenue / period_days if period_days > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'transaction_count': transaction_count,
        'avg_daily_revenue': avg_daily_revenue,
        'avg_transaction_value': avg_transaction_value,
        'growth_rate': growth_rate,
        'revenue_velocity': revenue_velocity
    }
