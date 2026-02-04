"""Basket Analysis Implementation"""


from collections import defaultdict
from itertools import combinations

def find_frequent_itemsets(transactions: list, min_support: float = 0.1) -> dict:
    item_counts = defaultdict(int)
    total_transactions = len(transactions)
    
    for transaction in transactions:
        items = transaction.get('items', [])
        for item in items:
            item_counts[item] += 1
    
    frequent_items = {
        item: count for item, count in item_counts.items()
        if count / total_transactions >= min_support
    }
    
    pair_counts = defaultdict(int)
    
    for transaction in transactions:
        items = transaction.get('items', [])
        frequent_in_transaction = [item for item in items if item in frequent_items]
        
        for pair in combinations(frequent_in_transaction, 2):
            pair_counts[tuple(sorted(pair))] += 1
    
    association_rules = []
    
    for pair, count in pair_counts.items():
        support = count / total_transactions
        
        if support >= min_support:
            item_a, item_b = pair
            
            confidence_a_to_b = count / item_counts[item_a]
            confidence_b_to_a = count / item_counts[item_b]
            
            lift = support * ((item_counts[item_a] / total_transactions) * (item_counts[item_b] / total_transactions))
            
            association_rules.append({
                'items': pair,
                'support': support,
                'lift': lift
            })
    
    association_rules.sort(key=lambda x: x['lift'], reverse=True)
    
    return {
        'association_rules': association_rules[:20]
    }

