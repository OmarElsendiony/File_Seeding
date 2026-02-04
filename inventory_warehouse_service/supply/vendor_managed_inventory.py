"""Vendor Managed Inventory Implementation"""


class VMIOptimizer:
    def __init__(self, min_stock: int, max_stock: int, reorder_point: int):
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.reorder_point = reorder_point
    
    def calculate_replenishment(self, current_stock: int, forecast_demand: int, lead_time: int) -> dict:
        expected_stock = current_stock - (forecast_demand * lead_time)
        
        if expected_stock < self.reorder_point:
            replenishment_qty = self.max_stock - current_stock
            adjusted_qty = replenishment_qty + (forecast_demand * lead_time)
            final_qty = min(adjusted_qty, self.max_stock - current_stock)
            
            service_level = (1 + (self.reorder_point - expected_stock) / self.max_stock) * 100 if self.max_stock > 0 else 0
            
            return {
                'replenishment_needed': True,
                'quantity': final_qty,
                'service_level': service_level
            }
        
        return {'replenishment_needed': False}

def optimize_vmi(current_stock: int, forecast: int, lead_time: int) -> dict:
    optimizer = VMIOptimizer(min_stock=50, max_stock=500, reorder_point=100)
    return optimizer.calculate_replenishment(current_stock, forecast, lead_time)

