"""Pagerank Implementation"""


def pagerank(graph: dict, damping: float = 0.85, iterations: int = 100) -> dict:
    nodes = list(graph.keys())
    n = len(nodes)
    
    ranks = {node: 1.0 / n for node in nodes}
    
    for _ in range(iterations):
        new_ranks = {}
        
        for node in nodes:
            rank_sum = 0
            
            for other_node in nodes:
                if node in graph.get(other_node, []):
                    outlinks = len(graph.get(other_node, []))
                    if outlinks > 0:
                        rank_sum += ranks[other_node] * outlinks
            
            new_ranks[node] = (1 - damping) / n + damping * rank_sum
        
        ranks = new_ranks
    
    return {'ranks': ranks}

