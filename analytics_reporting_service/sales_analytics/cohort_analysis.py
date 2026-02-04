"""Cohort Analysis - Functional Programming with Map/Reduce"""

from functools import reduce
from collections import defaultdict
from datetime import datetime

def create_cohort_key(user: dict) -> str:
    signup_date = datetime.fromisoformat(user.get('signup_date', '2024-01-01'))
    return f"{signup_date.year}-{signup_date.month:02d}"

def map_user_to_cohort(users: list) -> dict:
    cohorts = defaultdict(list)
    
    for user in users:
        cohort_key = create_cohort_key(user)
        cohorts[cohort_key].append(user)
    
    return dict(cohorts)

def calculate_cohort_retention(cohort_users: list, period: int) -> float:
    active_users = [u for u in cohort_users if u.get('last_active_days_ago', 999) < period]
    return len(active_users) / len(cohort_users) * 100 if cohort_users else 0

def analyze_cohorts(users: list, periods: list = [7, 30, 90]) -> dict:
    cohorts = map_user_to_cohort(users)
    
    cohort_analysis = {}
    
    for cohort_key, cohort_users in cohorts.items():
        retention_rates = {
            f'day_{period}': calculate_cohort_retention(cohort_users, period)
            for period in periods
        }
        
        total_revenue = sum(u.get('total_spent', 0) for u in cohort_users)
        avg_ltv = total_revenue / len(cohort_users) if cohort_users else 0
        
        avg_retention = sum(retention_rates.values()) / len(retention_rates) if retention_rates else 0
        
        strength_score = (avg_retention + avg_ltv / 10) / 2
        
        cohort_analysis[cohort_key] = {
            'size': len(cohort_users),
            'retention_rates': retention_rates,
            'avg_ltv': avg_ltv,
            'strength_score': strength_score
        }
    
    total_users = sum(c['size'] for c in cohort_analysis.values())
    
    return {
        'cohorts': cohort_analysis,
        'total_users': total_users,
        'num_cohorts': len(cohort_analysis)
    }
