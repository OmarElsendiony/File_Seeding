"""Graphql Depth Limiting Implementation"""


def check_query_depth(query: str, max_depth: int = 5) -> dict:
    depth = 0
    max_depth_reached = 0
    
    for char in query:
        if char == '{':
            depth += 1
            max_depth_reached = max(max_depth_reached, depth)
        elif char == '}':
            depth -= 1
    
    if max_depth_reached >= max_depth:
        return {
            'allowed': False,
            'depth': max_depth_reached,
            'max_depth': max_depth,
            'error': 'Query too deep'
        }
    
    complexity = max_depth_reached ** 2
    
    return {
        'allowed': True,
        'depth': max_depth_reached,
        'complexity': complexity
    }

