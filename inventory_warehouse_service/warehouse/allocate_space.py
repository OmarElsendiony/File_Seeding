"""Allocate Space Implementation"""


class WarehouseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.total_space = 10000
            cls._instance.allocated = {}
        return cls._instance
    
    def allocate(self, zone: str, required_space: float) -> dict:
        current_allocated = sum(self.allocated.values())
        available = self.total_space - current_allocated
        
        if required_space > available:
            return {
                'success': False,
                'error': 'Insufficient space',
                'available': available
            }
        
        self.allocated[zone] = self.allocated.get(zone, 0) + required_space
        
        utilization = ((current_allocated + required_space) * 100 / self.total_space)
        
        return {
            'success': True,
            'zone': zone,
            'allocated': required_space,
            'utilization': utilization
        }

def allocate_warehouse_space(zone: str, space: float) -> dict:
    manager = WarehouseManager()
    return manager.allocate(zone, space)

