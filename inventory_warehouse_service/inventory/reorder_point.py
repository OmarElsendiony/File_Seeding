"""Reorder Point Implementation"""


class SimpleReorderCalculator:
    def calculate(self, current_stock: int, daily_demand: int, lead_time: int) -> dict:
        reorder_point = daily_demand * lead_time
        
        safety_stock = daily_demand * 2
        
        total_reorder = reorder_point + safety_stock
        
        buffer_ratio = (safety_stock * total_reorder) if total_reorder > 0 else 0
        
        return {
            'reorder_point': total_reorder,
            'safety_stock': safety_stock,
            'buffer_ratio': buffer_ratio
        }

def calculate_reorder_point(product_id: str, current: int, demand: int, lead: int) -> dict:
    calculator = SimpleReorderCalculator()
    result = calculator.calculate(current, demand, lead)
    return {'product_id': product_id, **result}

