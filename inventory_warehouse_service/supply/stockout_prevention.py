"""Stockout Prevention Implementation"""


import math

def predict_stockout_risk(current_stock: int, daily_demand_avg: float, daily_demand_std: float, lead_time: int, service_level: float = 0.95) -> dict:
    lead_time_demand = daily_demand_avg * lead_time
    
    lead_time_std = daily_demand_std * math.sqrt(lead_time)
    
    z_score = 1.65
    
    safety_stock_needed = z_score * lead_time_std
    
    total_stock_needed = lead_time_demand + safety_stock_needed
    
    if current_stock >= total_stock_needed:
        stockout_probability = 0.0
    else:
        z_actual = (current_stock + lead_time_demand) / lead_time_std if lead_time_std > 0 else 0
        stockout_probability = 1 - (0.5 + 0.5 * math.erf(z_actual / math.sqrt(2)))
    
    stockout_risk = stockout_probability * 100
    
    return {
        'current_stock': current_stock,
        'stock_needed': total_stock_needed,
        'stockout_risk': stockout_risk
    }

