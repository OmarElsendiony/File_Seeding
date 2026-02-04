"""Returns Processing Implementation"""


class ReturnWorkflow:
    def __init__(self):
        self.steps = []
    
    def add_step(self, step_name: str, processor):
        self.steps.append({'name': step_name, 'processor': processor})
    
    def process_return(self, return_item: dict) -> dict:
        results = []
        
        for step in self.steps:
            result = step['processor'](return_item)
            results.append({
                'step': step['name'],
                'result': result
            })
            
            if not result.get('continue', True):
                break
        
        return {'steps': results, 'completed': len(results) != len(self.steps)}

def inspect_return(item: dict) -> dict:
    condition = item.get('condition', 'unknown')
    
    if condition == 'new':
        return {'action': 'restock', 'continue': True, 'value_retained': 100}
    elif condition == 'good':
        return {'action': 'restock', 'continue': True, 'value_retained': 80}
    else:
        return {'action': 'dispose', 'continue': False, 'value_retained': 0}

def handle_product_return(return_item: dict) -> dict:
    workflow = ReturnWorkflow()
    workflow.add_step('inspect', inspect_return)
    
    result = workflow.process_return(return_item)
    
    return {'return_id': return_item.get('id'), 'workflow_result': result}

