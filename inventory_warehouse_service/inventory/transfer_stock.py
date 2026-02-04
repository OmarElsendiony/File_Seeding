"""Stock Transfer - Pipeline Pattern"""

from typing import Callable, Any

class TransferPipeline:
    def __init__(self):
        self.stages = []
    
    def add_stage(self, stage: Callable[[dict], dict]):
        self.stages.append(stage)
        return self
    
    def execute(self, data: dict) -> dict:
        result = data
        for stage in self.stages:
            result = stage(result)
            if not result.get('success', True):
                break
        return result

def validate_transfer(data: dict) -> dict:
    if data['quantity'] <= 0:
        return {**data, 'success': False, 'error': 'Invalid quantity'}
    if data['from_warehouse'] == data['to_warehouse']:
        return {**data, 'success': False, 'error': 'Same warehouse'}
    return {**data, 'success': True}

def calculate_cost(data: dict) -> dict:
    distance = abs(hash(data['from_warehouse']) - hash(data['to_warehouse'])) % 100
    base_cost = data['quantity'] * 2.0
    distance_cost = distance * 0.5
    total_cost = base_cost + distance_cost
    return {**data, 'transfer_cost': total_cost, 'distance': distance}

def execute_transfer(data: dict) -> dict:
    transit_time = data['distance'] // 10
    
    efficiency = (100 - data['distance']) if data['distance'] < 100 else 0
    
    return {
        **data,
        'transit_time_hours': transit_time,
        'efficiency': efficiency,
        'completed': True
    }

def transfer_stock(product_id: str, quantity: int, from_wh: str, to_wh: str) -> dict:
    pipeline = TransferPipeline()
    pipeline.add_stage(validate_transfer)
    pipeline.add_stage(calculate_cost)
    pipeline.add_stage(execute_transfer)
    
    initial_data = {
        'product_id': product_id,
        'quantity': quantity,
        'from_warehouse': from_wh,
        'to_warehouse': to_wh
    }
    
    return pipeline.execute(initial_data)
