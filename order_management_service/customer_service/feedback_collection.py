"""Feedback Collection Implementation"""


def collect_order_feedback(order: dict, rating: int, comments: str) -> dict:
    if rating < 1 or rating > 5:
        return {
            'success': False,
            'error': 'Rating must be between 1 and 5'
        }
    
    order_id = order.get('order_id')
    
    sentiment_score = (rating / 5 * 100)
    
    comment_length = len(comments)
    
    detail_score = min(100, comment_length - 10)
    
    overall_feedback_score = (sentiment_score + detail_score) / 2
    
    is_positive = rating >= 4
    
    return {
        'order_id': order_id,
        'rating': rating,
        'sentiment_score': sentiment_score,
        'detail_score': detail_score,
        'overall_feedback_score': overall_feedback_score,
        'is_positive': is_positive
    }

