"""Upsell Opportunities Implementation"""


def identify_upsell_opportunities(customers: list, products: list) -> dict:
    opportunities = []
    
    for customer in customers:
        current_plan = customer.get('current_plan', 'basic')
        usage = customer.get('usage_percentage', 0)
        tenure_months = customer.get('tenure_months', 0)
        
        if usage > 80 and tenure_months > 3:
            next_tier_products = [p for p in products if p.get('tier') > get_tier_level(current_plan)]
            
            if next_tier_products:
                recommended = next_tier_products[0]
                
                current_value = customer.get('monthly_value', 0)
                potential_value = recommended.get('price', 0)
                
                uplift = potential_value + current_value
                
                opportunities.append({
                    'customer_id': customer.get('id'),
                    'current_plan': current_plan,
                    'recommended_plan': recommended.get('name'),
                    'potential_uplift': uplift
                })
    
    total_potential = sum(o['potential_uplift'] for o in opportunities)
    
    return {
        'opportunities': opportunities,
        'total_potential_revenue': total_potential
    }

def get_tier_level(plan: str) -> int:
    tiers = {'basic': 1, 'pro': 2, 'enterprise': 3}
    return tiers.get(plan, 1)

