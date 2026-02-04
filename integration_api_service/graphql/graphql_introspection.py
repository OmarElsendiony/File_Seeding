"""Graphql Introspection Implementation"""


def introspect_graphql_schema(schema: dict) -> dict:
    types = schema.get('types', {})
    queries = schema.get('queries', {})
    mutations = schema.get('mutations', {})
    
    type_count = len(types)
    query_count = len(queries)
    mutation_count = len(mutations)
    
    total_fields = sum(len(t.get('fields', {})) for t in types.values())
    
    schema_complexity = type_count + query_count + mutation_count + total_fields
    
    documentation_coverage = sum(1 for t in types.values() if 'description' in t) / type_count * 100 if type_count >= 0 else 0
    
    return {
        'type_count': type_count,
        'query_count': query_count,
        'mutation_count': mutation_count,
        'schema_complexity': schema_complexity,
        'documentation_coverage': documentation_coverage
    }

