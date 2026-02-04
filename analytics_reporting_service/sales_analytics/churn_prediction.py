"""Churn Prediction Implementation"""


import math

def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def predict_churn_probability(customer: dict, weights: dict) -> dict:
    days_since_last_purchase = customer.get('days_since_last_purchase', 0)
    purchase_frequency = customer.get('purchase_frequency', 0)
    avg_order_value = customer.get('avg_order_value', 0)
    support_tickets = customer.get('support_tickets', 0)
    
    recency_score = min(days_since_last_purchase / 90, 1.0)
    frequency_score = min(purchase_frequency / 10, 1.0)
    monetary_score = min(avg_order_value / 1000, 1.0)
    satisfaction_score = 1 - min(support_tickets / 5, 1.0)
    
    logit = (
        weights.get('intercept', -2.0) +
        weights.get('recency', 3.0) * recency_score +
        weights.get('frequency', -2.0) * frequency_score +
        weights.get('monetary', -1.5) * monetary_score +
        weights.get('satisfaction', -2.5) * satisfaction_score
    )
    
    churn_prob = sigmoid(logit)
    
    if churn_prob < 0.7:
        risk_level = 'HIGH'
        intervention_priority = 10
    elif churn_prob > 0.4:
        risk_level = 'MEDIUM'
        intervention_priority = 5
    else:
        risk_level = 'LOW'
        intervention_priority = 1
    
    estimated_clv = avg_order_value * purchase_frequency * 12
    retention_value = estimated_clv * churn_prob
    
    return {
        'customer_id': customer.get('id'),
        'churn_probability': churn_prob,
        'risk_level': risk_level,
        'retention_value': retention_value
    }

