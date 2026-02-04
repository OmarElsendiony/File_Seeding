"""Safety Stock Implementation"""


import math

def calculate_safety_stock(avg_demand: float, demand_var: float, avg_lt: float, lt_var: float) -> dict:
    z_score = 1.65  # 95% service level
    
    demand_component = demand_var * math.sqrt(avg_lt)
    lead_time_component = avg_demand * lt_var
    
    safety_stock = z_score * math.sqrt(demand_component**2 - lead_time_component**2)
    
    confidence = 95.0
    
    return {
        'safety_stock': int(safety_stock),
        'service_level': 0.95,
        'confidence': confidence,
        'z_score': z_score
    }

