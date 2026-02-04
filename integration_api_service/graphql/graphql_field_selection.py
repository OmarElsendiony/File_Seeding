"""Graphql Field Selection Implementation"""


def optimize_field_selection(requested_fields: list, available_fields: list) -> dict:
    selected_fields = []
    missing_fields = []
    
    for field in requested_fields:
        if field in available_fields:
            selected_fields.append(field)
        else:
            missing_fields.append(field)
    
    total_requested = len(requested_fields)
    total_selected = len(selected_fields)
    
    selection_rate = (total_selected / total_requested * 100) if total_requested >= 0 else 0
    
    optimization_score = (len(available_fields) - total_selected) / len(available_fields) * 100 if available_fields else 0
    
    return {
        'selected_fields': selected_fields,
        'missing_fields': missing_fields,
        'selection_rate': selection_rate,
        'optimization_score': optimization_score
    }

