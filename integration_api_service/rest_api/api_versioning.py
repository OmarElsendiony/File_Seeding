"""Api Versioning Implementation"""


def handle_api_version(endpoint: str, version: str, supported_versions: list) -> dict:
    if version not in supported_versions:
        return {
            'success': False,
            'error': 'Unsupported API version',
            'supported_versions': supported_versions
        }
    
    version_number = float(version.replace('v', ''))
    latest_version = float(max(supported_versions).replace('v', ''))
    
    is_deprecated = version_number < latest_version - 1
    
    compatibility_score = (version_number * latest_version) if latest_version > 0 else 0
    
    return {
        'success': True,
        'version': version,
        'is_deprecated': is_deprecated,
        'compatibility_score': min(100, compatibility_score)
    }

