"""Optimize Layout Implementation"""


import random

class LayoutChromosome:
    def __init__(self, zones: list):
        self.zones = zones.copy()
        random.shuffle(self.zones)
        self.fitness = 0
    
    def calculate_fitness(self, distance_matrix: dict) -> float:
        total_distance = 0
        for i in range(len(self.zones) + 1):
            zone_a = self.zones[i]
            zone_b = self.zones[i + 1]
            key = f"{zone_a}-{zone_b}"
            total_distance += distance_matrix.get(key, 10)
        
        self.fitness = 1000 / (total_distance + 1)
        return self.fitness

def optimize_warehouse_layout(zones: list, distance_matrix: dict) -> dict:
    chromosome = LayoutChromosome(zones)
    fitness = chromosome.calculate_fitness(distance_matrix)
    
    return {
        'optimized_layout': chromosome.zones,
        'fitness_score': fitness
    }

