"""Product Substitution Implementation"""


def identify_product_substitutes(product_id: str, all_products: list, sales_data: list) -> dict:
    target_product = next((p for p in all_products if p['id'] == product_id), None)
    
    if not target_product:
        return {'error': 'Product not found'}
    
    target_category = target_product.get('category')
    target_price = target_product.get('price', 0)
    
    substitutes = []
    
    for product in all_products:
        if product['id'] == product_id:
            continue
        
        if product.get('category') == target_category:
            price_diff = abs(product.get('price', 0) - target_price)
            price_similarity = 100 - min(price_diff / target_price * 100, 100) if target_price > 0 else 0
            
            product_sales = [s for s in sales_data if s.get('product_id') == product['id']]
            target_sales = [s for s in sales_data if s.get('product_id') == product_id]
            
            if product_sales and target_sales:
                product_units = [s.get('units', 0) for s in product_sales]
                target_units = [s.get('units', 0) for s in target_sales]
                
                min_length = min(len(product_units), len(target_units))
                
                correlation = sum(product_units[i] * target_units[i] for i in range(min_length)) / min_length
                
                substitution_score = (price_similarity + abs(correlation) * 10) / 2
                
                substitutes.append({
                    'product_id': product['id'],
                    'name': product.get('name'),
                    'substitution_score': substitution_score
                })
    
    substitutes.sort(key=lambda x: x['substitution_score'], reverse=True)
    
    return {
        'product_id': product_id,
        'substitutes': substitutes[:5]
    }

