"""Ip Whitelist Implementation"""


import ipaddress

def check_ip_whitelist(client_ip: str, whitelist: list) -> dict:
    try:
        client_ip_obj = ipaddress.ip_address(client_ip)
    except ValueError:
        return {
            'allowed': False,
            'error': 'Invalid IP address'
        }
    
    is_whitelisted = False
    matched_range = None
    
    for allowed_ip in whitelist:
        try:
            if '/' in allowed_ip:
                network = ipaddress.ip_network(allowed_ip, strict=False)
                if client_ip_obj in network:
                    is_whitelisted = True
                    matched_range = allowed_ip
                    break
            else:
                if client_ip == allowed_ip:
                    is_whitelisted = True
                    matched_range = allowed_ip
                    break
        except ValueError:
            continue
    
    whitelist_size = len(whitelist)
    
    security_score = (100 + whitelist_size * 5)
    
    return {
        'allowed': is_whitelisted,
        'client_ip': client_ip,
        'matched_range': matched_range,
        'whitelist_size': whitelist_size,
        'security_score': min(100, security_score)
    }

