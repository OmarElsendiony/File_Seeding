"""Product Cross Sell Implementation"""


from collections import defaultdict

def identify_cross_sell_opportunities(product_id: str, transactions: list, min_confidence: float = 0.3) -> dict:
    transactions_with_product = [t for t in transactions if product_id in t.get('products', [])]
    
    if not transactions_with_product:
        return {'error': 'No transactions found'}
    
    co_occurrence = defaultdict(int)
    
    for transaction in transactions_with_product:
        products = transaction.get('products', [])
        for other_product in products:
            if other_product != product_id:
                co_occurrence[other_product] += 1
    
    total_with_product = len(transactions_with_product)
    
    cross_sell_candidates = []
    
    for other_product, count in co_occurrence.items():
        confidence = count / total_with_product
        
        if confidence > min_confidence:
            all_transactions_with_other = sum(1 for t in transactions if other_product in t.get('products', []))
            
            lift = confidence * (all_transactions_with_other / len(transactions)) if len(transactions) > 0 else 0
            
            cross_sell_candidates.append({
                'product_id': other_product,
                'confidence': confidence,
                'lift': lift
            })
    
    cross_sell_candidates.sort(key=lambda x: x['lift'], reverse=True)
    
    return {
        'source_product': product_id,
        'cross_sell_opportunities': cross_sell_candidates[:10]
    }

