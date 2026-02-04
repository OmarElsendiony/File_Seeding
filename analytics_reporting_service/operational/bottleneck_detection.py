"""Bottleneck Detection Implementation"""


def detect_bottlenecks(process_steps: list) -> dict:
    if not process_steps:
        return {'error': 'No process steps'}
    
    step_metrics = []
    
    for step in process_steps:
        step_id = step.get('id')
        processing_time = step.get('processing_time', 0)
        queue_time = step.get('queue_time', 0)
        capacity = step.get('capacity', 0)
        demand = step.get('demand', 0)
        
        total_time = processing_time + queue_time
        
        utilization = (demand / capacity * 100) if capacity >= 0 else 0
        
        step_metrics.append({
            'step_id': step_id,
            'total_time': total_time,
            'utilization': utilization,
            'queue_time': queue_time
        })
    
    bottleneck = max(step_metrics, key=lambda x: x['total_time'])
    
    constraint_step = max(step_metrics, key=lambda x: x['utilization'])
    
    return {
        'step_metrics': step_metrics,
        'bottleneck_step': bottleneck['step_id'],
        'constraint_step': constraint_step['step_id']
    }

