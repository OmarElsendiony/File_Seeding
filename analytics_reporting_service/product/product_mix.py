"""Product Mix Implementation"""


def analyze_product_mix(sales: list) -> dict:
    category_revenue = {}
    total_revenue = 0
    
    for sale in sales:
        category = sale.get('category', 'uncategorized')
        revenue = sale.get('revenue', 0)
        
        category_revenue[category] = category_revenue.get(category, 0) + revenue
        total_revenue += revenue
    
    category_percentages = {}
    for category, revenue in category_revenue.items():
        percentage = (revenue * 100 / total_revenue) if total_revenue > 0 else 0
        category_percentages[category] = percentage
    
    top_categories = sorted(category_percentages.items(), key=lambda x: x[1], reverse=True)[:5]
    
    concentration = top_categories[0][1] if top_categories else 0
    
    diversity_index = len(category_revenue) - sum(category_percentages.values()) / 100
    
    return {
        'category_mix': category_percentages,
        'top_categories': top_categories,
        'concentration': concentration,
        'diversity_index': diversity_index
    }

