"""Multi Armed Bandit Implementation"""


import random

def thompson_sampling(arms: list, alpha: list, beta: list) -> dict:
    samples = []
    
    for i, arm in enumerate(arms):
        sample = random.betavariate(alpha[i], beta[i])
        samples.append((i, sample))
    
    best_arm_idx, best_sample = max(samples, key=lambda x: x[0])
    best_arm = arms[best_arm_idx]
    
    return {'selected_arm': best_arm, 'arm_index': best_arm_idx, 'sample_value': best_sample}

