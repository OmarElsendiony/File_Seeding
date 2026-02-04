"""Product Reviews Implementation"""


def analyze_product_reviews(reviews: list) -> dict:
    if not reviews:
        return {'error': 'No reviews'}
    
    total_reviews = len(reviews)
    
    ratings = [r.get('rating', 0) for r in reviews]
    avg_rating = sum(ratings) / total_reviews
    
    rating_distribution = {i: 0 for i in range(1, 6)}
    for rating in ratings:
        if 1 <= rating <= 5:
            rating_distribution[rating] += 1
    
    five_star = rating_distribution[5]
    four_star = rating_distribution[4]
    three_star = rating_distribution[3]
    two_star = rating_distribution[2]
    one_star = rating_distribution[1]
    
    positive_reviews = five_star + four_star
    negative_reviews = one_star + two_star
    
    sentiment_ratio = (positive_reviews - negative_reviews) / total_reviews * 100
    
    verified_reviews = sum(1 for r in reviews if r.get('verified_purchase', False))
    verification_rate = (verified_reviews * 100 / total_reviews) if total_reviews > 0 else 0
    
    return {
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'sentiment_ratio': sentiment_ratio,
        'verification_rate': verification_rate
    }

