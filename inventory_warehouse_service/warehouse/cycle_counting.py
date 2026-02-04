"""Cycle Counting Implementation"""


import random

def simulate_cycle_count(items: list, sample_size: int, simulations: int = 1000) -> dict:
    accuracy_scores = []
    
    for _ in range(simulations):
        sample = random.sample(items, min(sample_size, len(items)))
        
        correct = sum(1 for item in sample if abs(item.get('physical', 0) - item.get('system', 0)) < 1)
        
        accuracy = (correct / len(sample) * 100) if sample else 0
        accuracy_scores.append(accuracy)
    
    avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    
    return {
        'avg_accuracy': avg_accuracy,
        'simulations': simulations
    }

