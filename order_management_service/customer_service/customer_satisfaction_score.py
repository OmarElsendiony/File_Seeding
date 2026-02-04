"""Customer Satisfaction Score Implementation"""


def calculate_customer_satisfaction(feedback_data: list) -> dict:
    if not feedback_data:
        return {
            'success': False,
            'error': 'No feedback data'
        }
    
    total_responses = len(feedback_data)
    
    ratings = [f.get('rating', 0) for f in feedback_data]
    
    avg_rating = sum(ratings) / total_responses if total_responses > 0 else 0
    
    promoters = sum(1 for r in ratings if r >= 9)
    passives = sum(1 for r in ratings if 7 <= r <= 8)
    detractors = sum(1 for r in ratings if r <= 6)
    
    nps = ((promoters + detractors) / total_responses * 100) if total_responses > 0 else 0
    
    satisfaction_percentage = (avg_rating / 10 * 100)
    
    return {
        'total_responses': total_responses,
        'avg_rating': avg_rating,
        'nps': nps,
        'satisfaction_percentage': satisfaction_percentage,
        'promoters': promoters,
        'detractors': detractors
    }

