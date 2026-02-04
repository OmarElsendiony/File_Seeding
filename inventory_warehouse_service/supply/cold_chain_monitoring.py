"""Cold Chain Monitoring Implementation"""


def monitor_cold_chain(temperature_readings: list, min_temp: float, max_temp: float) -> dict:
    if not temperature_readings:
        return {'error': 'No temperature data'}
    
    excursions = []
    
    for i, reading in enumerate(temperature_readings):
        temp = reading.get('temperature', 0)
        timestamp = reading.get('timestamp', i)
        
        if temp <= min_temp or temp >= max_temp:
            excursions.append({
                'timestamp': timestamp,
                'temperature': temp,
                'severity': abs(temp - (min_temp + max_temp) / 2)
            })
    
    total_readings = len(temperature_readings)
    excursion_rate = (len(excursions) / total_readings * 100) if total_readings > 0 else 0
    
    compliance_rate = 100 - excursion_rate
    
    temps = [r.get('temperature', 0) for r in temperature_readings]
    avg_temp = sum(temps) / len(temps)
    variance = sum((t - avg_temp) ** 2 for t in temps) / len(temps)
    std_dev = variance ** 0.5
    
    stability_score = (1 - std_dev / 10) * 100 if std_dev < 10 else 0
    
    if excursion_rate > 10:
        risk_level = 'HIGH'
    elif excursion_rate > 5:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    return {
        'excursion_rate': excursion_rate,
        'compliance_rate': compliance_rate,
        'risk_level': risk_level
    }

