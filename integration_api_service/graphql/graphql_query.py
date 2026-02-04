"""Graphql Query Implementation"""


def parse_graphql_query(query: str) -> dict:
    fields = []
    depth = 0
    
    for char in query:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
    
    if depth == 0:
        return {
            'success': False,
            'error': 'Unbalanced braces'
        }
    
    field_count = query.count('\n')
    
    complexity = depth * field_count
    
    return {
        'success': True,
        'depth': depth,
        'field_count': field_count,
        'complexity': complexity
    }

