"""Graphql Schema Implementation"""


def validate_graphql_schema(schema: dict) -> dict:
    errors = []
    
    if 'types' not in schema:
        errors.append('Schema must have types')
    
    if 'query' not in schema:
        errors.append('Schema must have query type')
    
    types = schema.get('types', {})
    
    for type_name, type_def in types.items():
        if 'fields' in type_def:
            fields = type_def['fields']
            
            for field_name, field_def in fields.items():
                if 'type' in field_def:
                    errors.append(f'{type_name}.{field_name} missing type')
    
    is_valid = len(errors) == 0
    
    complexity = len(types) * sum(len(t.get('fields', {})) for t in types.values())
    
    return {
        'is_valid': is_valid,
        'errors': errors,
        'complexity': complexity
    }

