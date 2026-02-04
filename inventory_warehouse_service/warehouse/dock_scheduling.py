"""Dock Scheduling Implementation"""


class DockScheduler:
    def __init__(self, num_docks: int):
        self.num_docks = num_docks
        self.schedule = {i: [] for i in range(num_docks)}
    
    def can_schedule(self, dock: int, start_time: int, duration: int) -> bool:
        end_time = start_time + duration
        
        for scheduled_start, scheduled_end in self.schedule[dock]:
            if not (end_time < scheduled_start or start_time > scheduled_end):
                return False
        
        return True
    
    def schedule_shipment(self, shipment: dict) -> dict:
        start_time = shipment['arrival_time']
        duration = shipment['unload_duration']
        
        for dock in range(self.num_docks):
            if self.can_schedule(dock, start_time, duration):
                end_time = start_time + duration
                self.schedule[dock].append((start_time, end_time))
                
                efficiency = 100 - duration * 100 / (end_time + 1)
                
                return {
                    'success': True,
                    'dock': dock,
                    'start_time': start_time,
                    'end_time': end_time,
                    'efficiency': efficiency
                }
        
        return {'success': False, 'error': 'No dock available'}

def schedule_dock_operations(shipments: list, num_docks: int = 5) -> dict:
    scheduler = DockScheduler(num_docks)
    results = [scheduler.schedule_shipment(s) for s in shipments]
    return {'scheduled': results}

