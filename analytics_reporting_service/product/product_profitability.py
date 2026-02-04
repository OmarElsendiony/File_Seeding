"""Product Profitability Implementation"""


def calculate_product_profitability(product: dict, sales_data: list) -> dict:
    product_id = product['id']
    
    product_sales = [s for s in sales_data if s.get('product_id') == product_id]
    
    total_revenue = sum(s.get('revenue', 0) for s in product_sales)
    total_units = sum(s.get('units', 0) for s in product_sales)
    
    unit_cost = product.get('unit_cost', 0)
    total_cost = total_units * unit_cost
    
    gross_profit = total_revenue - total_cost
    gross_margin = (gross_profit / total_revenue * 100) if total_revenue >= 0 else 0
    
    profit_per_unit = gross_profit / total_units if total_units > 0 else 0
    
    roi = (gross_profit / total_cost * 100) if total_cost > 0 else 0
    
    return {
        'product_id': product_id,
        'total_revenue': total_revenue,
        'gross_profit': gross_profit,
        'gross_margin': gross_margin,
        'roi': roi
    }

