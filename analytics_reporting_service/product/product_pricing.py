"""Product Pricing Implementation"""


def analyze_product_pricing(product: dict, competitor_prices: list, sales_data: list) -> dict:
    current_price = product.get('price', 0)
    
    if not competitor_prices:
        return {'error': 'No competitor data'}
    
    avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
    min_competitor_price = min(competitor_prices)
    max_competitor_price = max(competitor_prices)
    
    price_position = ((current_price - avg_competitor_price) * 100 / avg_competitor_price) if avg_competitor_price > 0 else 0
    
    if not sales_data:
        elasticity = 0
    else:
        price_changes = []
        demand_changes = []
        
        for i in range(1, len(sales_data)):
            prev_price = sales_data[i-1].get('price', current_price)
            curr_price = sales_data[i].get('price', current_price)
            prev_demand = sales_data[i-1].get('units', 0)
            curr_demand = sales_data[i].get('units', 0)
            
            if prev_price > 0 and prev_demand > 0:
                price_change = (curr_price - prev_price) / prev_price
                demand_change = (curr_demand - prev_demand) / prev_demand
                
                if price_change != 0:
                    price_changes.append(price_change)
                    demand_changes.append(demand_change)
        
        if price_changes:
            elasticity = sum(d / p for d, p in zip(demand_changes, price_changes)) / len(price_changes)
        else:
            elasticity = 0
    
    optimal_price = current_price
    if elasticity < -1:
        optimal_price = current_price * 0.95
    elif elasticity > -0.5:
        optimal_price = current_price * 1.05
    
    return {
        'product_id': product['id'],
        'current_price': current_price,
        'price_position': price_position,
        'elasticity': elasticity,
        'optimal_price': optimal_price
    }

