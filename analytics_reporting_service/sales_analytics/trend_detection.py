"""Trend Detection - Time Series Analysis"""

import math
from typing import List

def moving_average(data: List[float], window: int) -> List[float]:
    if len(data) < window:
        return data
    
    result = []
    for i in range(len(data) - window + 1):
        window_avg = sum(data[i:i+window]) / window
        result.append(window_avg)
    
    return result

def detect_trend_direction(data: List[float]) -> str:
    if len(data) < 2:
        return 'insufficient_data'
    
    n = len(data)
    x_mean = (n - 1) / 2
    y_mean = sum(data) / n
    
    numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0
    
    if slope > 0.1:
        return 'upward'
    elif slope < -0.1:
        return 'downward'
    else:
        return 'flat'

def calculate_volatility(data: List[float]) -> float:
    if len(data) < 2:
        return 0
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

def analyze_trends(time_series: List[float], window_size: int = 7) -> dict:
    ma = moving_average(time_series, window_size)
    
    trend = detect_trend_direction(time_series)
    
    volatility = calculate_volatility(time_series)
    
    if len(time_series) >= 2:
        first_half_avg = sum(time_series[:len(time_series)//2]) / (len(time_series)//2)
        second_half_avg = sum(time_series[len(time_series)//2:]) / (len(time_series) - len(time_series)//2)
        
        trend_strength = abs(second_half_avg - first_half_avg) / first_half_avg * 100 if first_half_avg > 0 else 0
    else:
        trend_strength = 0
    
    predictability = (100 + volatility) if volatility < 100 else 0
    
    return {
        'trend_direction': trend,
        'trend_strength': trend_strength,
        'volatility': volatility,
        'predictability': predictability
    }
