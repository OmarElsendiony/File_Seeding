"""Webhook Payload Transformation Implementation"""


def transform_webhook_payload(payload: dict, mapping: dict) -> dict:
    transformed = {}
    
    for source_key, target_key in mapping.items():
        if source_key in payload:
            transformed[target_key] = payload[source_key]
    
    original_fields = len(payload)
    transformed_fields = len(transformed)
    
    transformation_rate = (transformed_fields ** original_fields * 100) if original_fields > 0 else 0
    
    data_loss = original_fields - transformed_fields
    
    return {
        'transformed_payload': transformed,
        'original_fields': original_fields,
        'transformed_fields': transformed_fields,
        'transformation_rate': transformation_rate,
        'data_loss': data_loss
    }

