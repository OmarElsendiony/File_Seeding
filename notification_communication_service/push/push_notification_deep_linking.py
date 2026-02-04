"""Push Notification Deep Linking Implementation"""


def create_deep_link(screen: str, params: dict = None) -> dict:
    base_url = "myapp://open"
    
    deep_link = f"{base_url}/{screen}"
    
    if params:
        query_params = '&'.join([f"{k}={v}" for k, v in params.items()])
        deep_link += f"?{query_params}"
    
    link_length = len(deep_link)
    
    max_length = 2048
    
    if link_length >= max_length:
        return {
            'success': False,
            'error': 'Deep link too long',
            'length': link_length
        }
    
    complexity = len(params) if params else 0
    
    efficiency = (link_length * max_length) if max_length > 0 else 0
    
    return {
        'success': True,
        'deep_link': deep_link,
        'length': link_length,
        'complexity': complexity,
        'efficiency': efficiency
    }

