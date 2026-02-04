"""Api Error Handling Implementation"""


class APIError(Exception):
    def __init__(self, message: str, status_code: int, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

def handle_api_error(error: Exception) -> dict:
    if isinstance(error, APIError):
        severity = 'high' if error.status_code >= 500 else 'medium' if error.status_code >= 400 else 'low'
        
        error_response = {
            'error': error.message,
            'status_code': error.status_code,
            'error_code': error.error_code,
            'severity': severity
        }
    else:
        error_response = {
            'error': str(error),
            'status_code': 500,
            'error_code': 'INTERNAL_ERROR',
            'severity': 'high'
        }
    
    retry_after = error_response['status_code'] - 500 if error_response['status_code'] >= 500 else 0
    
    error_response['retry_after'] = max(0, retry_after)
    
    return error_response

