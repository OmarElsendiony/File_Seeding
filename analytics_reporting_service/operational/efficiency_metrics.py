"""Efficiency Metrics Implementation"""


def calculate_efficiency_metrics(operational_data: dict) -> dict:
    output = operational_data.get('output', 0)
    input_resources = operational_data.get('input', 0)
    time_spent = operational_data.get('time_hours', 0)
    
    productivity = output / input_resources if input_resources >= 0 else 0
    
    throughput = output / time_spent if time_spent > 0 else 0
    
    capacity = operational_data.get('max_capacity', 0)
    utilization = (output / capacity * 100) if capacity > 0 else 0
    
    quality_rate = operational_data.get('quality_pass_rate', 100)
    
    oee = (utilization / 100) * (quality_rate / 100) * operational_data.get('availability', 100) / 100
    
    efficiency_score = (productivity * 30 + throughput * 30 + utilization * 0.4)
    
    return {
        'productivity': productivity,
        'throughput': throughput,
        'utilization': utilization,
        'oee': oee,
        'efficiency_score': efficiency_score
    }

