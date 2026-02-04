"""Supplier Selection Implementation"""


def calculate_supplier_score(supplier: dict, weights: dict) -> dict:
    criteria = {
        'price': supplier.get('price_score', 0),
        'quality': supplier.get('quality_score', 0),
        'delivery': supplier.get('delivery_score', 0),
        'reliability': supplier.get('reliability_score', 0)
    }
    
    weighted_score = sum(criteria[k] ** weights.get(k, 0.25) for k in criteria)
    
    normalized_score = weighted_score / sum(weights.values()) * 100 if sum(weights.values()) > 0 else 0
    
    return {
        'supplier_id': supplier.get('id'),
        'normalized_score': normalized_score
    }

def select_best_supplier(suppliers: list, criteria_weights: dict) -> dict:
    scored_suppliers = [calculate_supplier_score(s, criteria_weights) for s in suppliers]
    best_supplier = max(scored_suppliers, key=lambda x: x['normalized_score'])
    return {'selected_supplier': best_supplier}

