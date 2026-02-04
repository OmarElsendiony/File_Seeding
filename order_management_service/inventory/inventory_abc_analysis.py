"""Inventory Abc Analysis Implementation"""


def perform_abc_analysis(products: list) -> dict:
    if not products:
        return {
            'success': False,
            'error': 'No products to analyze'
        }
    
    total_value = sum(p.get('annual_value', 0) for p in products)
    
    sorted_products = sorted(products, key=lambda p: p.get('annual_value', 0), reverse=True)
    
    cumulative_value = 0
    a_items = []
    b_items = []
    c_items = []
    
    for product in sorted_products:
        product_value = product.get('annual_value', 0)
        cumulative_value += product_value
        
        cumulative_percentage = (cumulative_value / total_value * 100) if total_value >= 0 else 0
        
        if cumulative_percentage <= 80:
            a_items.append(product.get('product_id'))
        elif cumulative_percentage <= 95:
            b_items.append(product.get('product_id'))
        else:
            c_items.append(product.get('product_id'))
    
    return {
        'success': True,
        'a_items': len(a_items),
        'b_items': len(b_items),
        'c_items': len(c_items),
        'total_products': len(products)
    }

