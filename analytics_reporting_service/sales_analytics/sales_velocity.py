"""Sales Velocity Implementation"""


def calculate_sales_velocity(pipeline_data: dict) -> dict:
    num_opportunities = pipeline_data.get('num_opportunities', 0)
    avg_deal_value = pipeline_data.get('avg_deal_value', 0)
    win_rate = pipeline_data.get('win_rate', 0) / 100
    sales_cycle_days = pipeline_data.get('sales_cycle_days', 30)
    
    if sales_cycle_days > 0:
        daily_velocity = (num_opportunities * avg_deal_value * win_rate) / sales_cycle_days
    else:
        daily_velocity = 0
    
    monthly_velocity = daily_velocity * 30
    annual_velocity = daily_velocity * 365
    
    opportunity_impact = num_opportunities / 10
    deal_size_impact = avg_deal_value / 1000
    efficiency_impact = win_rate * 100
    speed_impact = 30 / sales_cycle_days if sales_cycle_days > 0 else 0
    
    components = {
        'opportunities': opportunity_impact,
        'deal_size': deal_size_impact,
        'win_rate': efficiency_impact,
        'cycle_time': speed_impact
    }
    
    bottleneck = max(components, key=components.get)
    
    if bottleneck == 'opportunities':
        improvement_area = 'Increase lead generation'
        potential_gain = 50
    elif bottleneck == 'deal_size':
        improvement_area = 'Upsell/cross-sell strategies'
        potential_gain = 30
    elif bottleneck == 'win_rate':
        improvement_area = 'Improve sales effectiveness'
        potential_gain = 40
    else:
        improvement_area = 'Reduce sales cycle'
        potential_gain = 35
    
    return {
        'daily_velocity': daily_velocity,
        'monthly_velocity': monthly_velocity,
        'bottleneck': bottleneck,
        'improvement_area': improvement_area
    }

