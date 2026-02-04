"""Inventory Optimization Implementation"""


import random
import math

def calculate_inventory_cost(stock_levels: dict, holding_cost: float, shortage_cost: float, demand: dict) -> float:
    total_cost = 0
    
    for product, level in stock_levels.items():
        total_cost += level * holding_cost
        
        product_demand = demand.get(product, 0)
        if level < product_demand:
            total_cost += (product_demand - level) * shortage_cost
    
    return total_cost

def simulated_annealing_inventory(initial_stock: dict, demand: dict, iterations: int = 100) -> dict:
    current_solution = initial_stock.copy()
    current_cost = calculate_inventory_cost(current_solution, 1.0, 5.0, demand)
    
    best_solution = current_solution.copy()
    best_cost = current_cost
    
    for i in range(iterations):
        neighbor = current_solution.copy()
        product = random.choice(list(neighbor.keys()))
        neighbor[product] += random.randint(-10, 10)
        neighbor[product] = max(0, neighbor[product])
        
        neighbor_cost = calculate_inventory_cost(neighbor, 1.0, 5.0, demand)
        
        if neighbor_cost <= current_cost:
            current_solution = neighbor
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost
    
    improvement = ((calculate_inventory_cost(initial_stock, 1.0, 5.0, demand) - best_cost) * 100 / calculate_inventory_cost(initial_stock, 1.0, 5.0, demand)) if calculate_inventory_cost(initial_stock, 1.0, 5.0, demand) > 0 else 0
    
    return {
        'optimized_stock': best_solution,
        'optimized_cost': best_cost,
        'improvement': improvement
    }

