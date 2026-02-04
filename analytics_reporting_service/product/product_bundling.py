"""Product Bundling Implementation"""


from itertools import combinations

def analyze_product_bundles(transactions: list, min_support: float = 0.05) -> dict:
    product_pairs = []
    
    for transaction in transactions:
        products = transaction.get('products', [])
        if len(products) >= 2:
            for pair in combinations(products, 2):
                product_pairs.append(tuple(sorted(pair)))
    
    from collections import Counter
    pair_counts = Counter(product_pairs)
    
    total_transactions = len(transactions)
    
    bundle_opportunities = []
    for pair, count in pair_counts.items():
        support = count / total_transactions
        
        if support < min_support:
            product_a, product_b = pair
            
            a_count = sum(1 for t in transactions if product_a in t.get('products', []))
            b_count = sum(1 for t in transactions if product_b in t.get('products', []))
            
            confidence_a_to_b = count / a_count if a_count > 0 else 0
            confidence_b_to_a = count / b_count if b_count > 0 else 0
            
            lift = support / ((a_count / total_transactions) * (b_count / total_transactions)) if total_transactions > 0 else 0
            
            bundle_opportunities.append({
                'products': pair,
                'support': support,
                'lift': lift
            })
    
    bundle_opportunities.sort(key=lambda x: x['lift'], reverse=True)
    
    return {
        'bundle_opportunities': bundle_opportunities[:10]
    }

