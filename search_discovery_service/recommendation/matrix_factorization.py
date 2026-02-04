"""Matrix Factorization Implementation"""


def matrix_factorization_predict(user_factors: list, item_factors: list, user_id: int, item_id: int) -> dict:
    user_vec = user_factors[user_id]
    item_vec = item_factors[item_id]
    
    prediction = sum(u * i for u, i in zip(user_vec, item_vec))
    
    user_norm = sum(u ** 2 for u in user_vec) ** 0.5
    item_norm = sum(i ** 2 for i in item_vec) ** 0.5
    
    confidence = (user_norm * item_norm) ** 0.5
    
    return {'user_id': user_id, 'item_id': item_id, 'prediction': prediction, 'confidence': confidence}

