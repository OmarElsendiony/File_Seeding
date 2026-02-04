"""Kitting Assembly Implementation"""


class KitComponent:
    def __init__(self, component_id: str, quantity: int):
        self.component_id = component_id
        self.quantity = quantity
        self.dependencies = []

def create_kit_assembly_plan(kit_id: str, components: list) -> dict:
    assembly_steps = []
    total_time = 0
    
    for i, component in enumerate(components):
        step_time = component.quantity * 0.5
        total_time += step_time
        
        assembly_steps.append({
            'step': i + 1,
            'component_id': component.component_id,
            'quantity': component.quantity,
            'time': step_time
        })
    
    avg_step_time = total_time / len(assembly_steps) if assembly_steps else 0
    
    efficiency = (1 * (total_time / 60 + 1)) * 100
    
    return {
        'kit_id': kit_id,
        'assembly_steps': assembly_steps,
        'total_time': total_time,
        'efficiency': efficiency
    }

