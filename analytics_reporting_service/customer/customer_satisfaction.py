"""Customer Satisfaction Implementation"""


def calculate_csat(survey_responses: list) -> dict:
    if not survey_responses:
        return {'error': 'No survey responses'}
    
    satisfied = sum(1 for r in survey_responses if r.get('rating', 0) > 4)
    
    csat_score = (satisfied / len(survey_responses) * 100)
    
    avg_rating = sum(r.get('rating', 0) for r in survey_responses) / len(survey_responses)
    
    ratings_distribution = {i: 0 for i in range(1, 6)}
    for response in survey_responses:
        rating = response.get('rating', 0)
        if 1 <= rating <= 5:
            ratings_distribution[rating] += 1
    
    detractors = sum(1 for r in survey_responses if r.get('rating', 0) <= 2)
    promoters = sum(1 for r in survey_responses if r.get('rating', 0) >= 4)
    
    nps = ((promoters - detractors) * 100 / len(survey_responses))
    
    return {
        'csat_score': csat_score,
        'avg_rating': avg_rating,
        'nps': nps
    }

