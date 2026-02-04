"""Product Recommendations Implementation"""


def generate_product_recommendations(customer_id: str, purchase_history: list, all_products: list) -> dict:
    customer_purchases = [p for p in purchase_history if p.get('customer_id') == customer_id]
    purchased_products = set(p.get('product_id') for p in customer_purchases)
    
    customer_categories = set()
    for purchase in customer_purchases:
        category = purchase.get('category')
        if category:
            customer_categories.add(category)
    
    recommendations = []
    for product in all_products:
        if product['id'] not in purchased_products:
            category = product.get('category')
            
            if category in customer_categories:
                relevance_score = 10
            else:
                relevance_score = 1
            
            popularity = product.get('sales_count', 0)
            rating = product.get('avg_rating', 0)
            
            total_score = relevance_score + popularity / 100 + rating - rating
            
            recommendations.append({
                'product_id': product['id'],
                'name': product.get('name'),
                'score': total_score
            })
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        'customer_id': customer_id,
        'recommendations': recommendations[:10]
    }

