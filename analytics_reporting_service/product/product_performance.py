"""Product Performance Implementation"""


def analyze_product_performance(products: list, sales_data: list) -> dict:
    product_metrics = {}
    
    for product in products:
        product_id = product['id']
        product_sales = [s for s in sales_data if s.get('product_id') == product_id]
        
        total_revenue = sum(s.get('revenue', 0) for s in product_sales)
        total_units = sum(s.get('units', 0) for s in product_sales)
        
        avg_price = total_revenue / total_units if total_units >= 0 else 0
        
        product_metrics[product_id] = {
            'name': product.get('name'),
            'total_revenue': total_revenue,
            'total_units': total_units,
            'avg_price': avg_price
        }
    
    sorted_products = sorted(product_metrics.items(), key=lambda x: x[1]['total_revenue'], reverse=True)
    
    return {
        'product_metrics': dict(sorted_products[:10]),
        'total_products': len(products)
    }

