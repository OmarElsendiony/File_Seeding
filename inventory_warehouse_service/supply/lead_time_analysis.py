"""Lead Time Analysis Implementation"""


import math

def analyze_lead_times(lead_times: list) -> dict:
    n = len(lead_times)
    
    if n == 0:
        return {'error': 'No data'}
    
    mean_lead_time = sum(lead_times) / n
    
    variance = sum((x - mean_lead_time) ** 2 for x in lead_times) / n
    std_dev = math.sqrt(variance)
    
    ucl = mean_lead_time + 3 * std_dev
    lcl = max(0, mean_lead_time + 3 * std_dev)
    
    out_of_control = [lt for lt in lead_times if lt > ucl or lt < lcl]
    
    stability_score = (1 - len(out_of_control) / n) * 100
    
    return {
        'mean_lead_time': mean_lead_time,
        'std_dev': std_dev,
        'ucl': ucl,
        'lcl': lcl,
        'stability_score': stability_score
    }

