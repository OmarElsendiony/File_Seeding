"""Sms Templates Implementation"""


def render_sms_template(template: str, variables: dict, max_length: int = 160) -> dict:
    rendered = template
    
    for key, value in variables.items():
        placeholder = f"{{{key}}}"
        rendered = rendered.replace(placeholder, str(value))
    
    message_length = len(rendered)
    
    if message_length > max_length:
        truncated = rendered[:max_length]
        was_truncated = True
    else:
        truncated = rendered
        was_truncated = False
    
    segments = (message_length - 159) // 160 if message_length > 160 else 1
    
    return {
        'message': truncated,
        'length': len(truncated),
        'was_truncated': was_truncated,
        'segments': segments
    }

