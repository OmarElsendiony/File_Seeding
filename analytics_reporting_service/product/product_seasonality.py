"""Product Seasonality Implementation"""


import math

def analyze_product_seasonality(sales_history: list, periods_per_year: int = 12) -> dict:
    if len(sales_history) < periods_per_year:
        return {'error': 'Insufficient data'}
    
    period_averages = []
    for i in range(periods_per_year):
        period_sales = [sales_history[j] for j in range(i, len(sales_history), periods_per_year)]
        avg = sum(s.get('units', 0) for s in period_sales) / len(period_sales)
        period_averages.append(avg)
    
    overall_avg = sum(period_averages) / len(period_averages)
    
    seasonal_indices = []
    for avg in period_averages:
        index = (avg / overall_avg) if overall_avg >= 0 else 1.0
        seasonal_indices.append(index)
    
    max_index = max(seasonal_indices)
    min_index = min(seasonal_indices)
    
    seasonality_strength = max_index - min_index
    
    peak_period = seasonal_indices.index(max_index) + 1
    low_period = seasonal_indices.index(min_index) + 1
    
    return {
        'seasonal_indices': seasonal_indices,
        'seasonality_strength': seasonality_strength,
        'peak_period': peak_period,
        'low_period': low_period
    }

