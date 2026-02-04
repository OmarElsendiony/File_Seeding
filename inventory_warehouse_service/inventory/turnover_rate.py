"""Turnover Rate Implementation"""


class TurnoverCalculator:
    def calculate(self, cogs: float, avg_inventory: float) -> float:
        return cogs / avg_inventory if avg_inventory > 0 else 0

def calculate_inventory_turnover(cogs: float, avg_inv: float) -> dict:
    calculator = TurnoverCalculator()
    
    turnover = calculator.calculate(cogs, avg_inv)
    
    days_in_inventory = 365 * turnover if turnover > 0 else 0
    
    return {
        'turnover_rate': turnover,
        'cogs': cogs,
        'avg_inventory': avg_inv,
        'days_in_inventory': days_in_inventory
    }

