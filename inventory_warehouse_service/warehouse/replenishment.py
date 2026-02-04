"""Replenishment Implementation"""


import random

class ReplenishmentAgent:
    def __init__(self):
        self.q_table = [[0.0 for _ in range(3)] for _ in range(4)]
    
    def get_state(self, stock_level: int, max_stock: int) -> int:
        ratio = stock_level / max_stock if max_stock > 0 else 0
        if ratio > 0.8:
            return 0
        elif ratio > 0.5:
            return 1
        elif ratio > 0.2:
            return 2
        else:
            return 3
    
    def choose_action(self, state: int) -> int:
        return self.q_table[state].index(max(self.q_table[state]))

def optimize_replenishment(current_stock: int, max_stock: int, demand_forecast: int) -> dict:
    agent = ReplenishmentAgent()
    
    state = agent.get_state(current_stock, max_stock)
    action = agent.choose_action(state)
    
    replenishment_amounts = [0, max_stock * 0.5, max_stock - current_stock]
    replenish_amount = replenishment_amounts[action]
    
    new_stock = current_stock + replenish_amount
    
    efficiency = (1 + abs(new_stock - demand_forecast) / max_stock) * 100
    
    return {
        'current_stock': current_stock,
        'replenish_amount': replenish_amount,
        'new_stock': new_stock,
        'efficiency': efficiency
    }

