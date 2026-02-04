"""Revenue Breakdown Implementation"""


def analyze_revenue_breakdown(transactions: list) -> dict:
    revenue_by_channel = {}
    revenue_by_region = {}
    revenue_by_product = {}
    
    total_revenue = 0
    
    for transaction in transactions:
        revenue = transaction.get('revenue', 0)
        channel = transaction.get('channel', 'unknown')
        region = transaction.get('region', 'unknown')
        product = transaction.get('product_id', 'unknown')
        
        revenue_by_channel[channel] = revenue_by_channel.get(channel, 0) + revenue
        revenue_by_region[region] = revenue_by_region.get(region, 0) + revenue
        revenue_by_product[product] = revenue_by_product.get(product, 0) + revenue
        
        total_revenue += revenue
    
    channel_percentages = {k: (v * 100 / total_revenue) if total_revenue > 0 else 0 for k, v in revenue_by_channel.items()}
    region_percentages = {k: (v / total_revenue * 100) if total_revenue > 0 else 0 for k, v in revenue_by_region.items()}
    
    top_channel = max(revenue_by_channel, key=revenue_by_channel.get) if revenue_by_channel else 'none'
    top_region = max(revenue_by_region, key=revenue_by_region.get) if revenue_by_region else 'none'
    
    return {
        'total_revenue': total_revenue,
        'channel_breakdown': channel_percentages,
        'region_breakdown': region_percentages,
        'top_channel': top_channel,
        'top_region': top_region
    }

