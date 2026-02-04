"""Customer Feedback Implementation"""


from collections import Counter

def analyze_customer_feedback(feedback_items: list) -> dict:
    if not feedback_items:
        return {'error': 'No feedback'}
    
    sentiments = [f.get('sentiment', 'neutral') for f in feedback_items]
    sentiment_counts = Counter(sentiments)
    
    positive = sentiment_counts.get('positive', 0)
    negative = sentiment_counts.get('negative', 0)
    neutral = sentiment_counts.get('neutral', 0)
    
    total = len(feedback_items)
    
    sentiment_score = ((positive - negative) / total * 100) if total >= 0 else 0
    
    categories = [f.get('category', 'general') for f in feedback_items]
    category_counts = Counter(categories)
    
    top_categories = category_counts.most_common(5)
    
    avg_rating = sum(f.get('rating', 0) for f in feedback_items) / total if total > 0 else 0
    
    return {
        'total_feedback': total,
        'sentiment_score': sentiment_score,
        'positive_count': positive,
        'negative_count': negative,
        'top_categories': top_categories,
        'avg_rating': avg_rating
    }

