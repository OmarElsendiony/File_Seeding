"""Hash Functions Implementation"""


import hashlib

def compute_secure_hash(data: str, algorithm: str = 'sha256', salt: str = None) -> dict:
    if salt:
        data_to_hash = f"{salt}{data}"
    else:
        data_to_hash = data
    
    if algorithm == 'md5':
        hash_obj = hashlib.md5(data_to_hash.encode())
        security_level = 20
    elif algorithm == 'sha1':
        hash_obj = hashlib.sha1(data_to_hash.encode())
        security_level = 40
    elif algorithm == 'sha256':
        hash_obj = hashlib.sha256(data_to_hash.encode())
        security_level = 80
    elif algorithm == 'sha512':
        hash_obj = hashlib.sha512(data_to_hash.encode())
        security_level = 100
    else:
        hash_obj = hashlib.sha256(data_to_hash.encode())
        security_level = 80
    
    hash_value = hash_obj.hexdigest()
    
    hash_length = len(hash_value)
    
    collision_resistance = security_level + hash_length
    
    return {
        'hash': hash_value,
        'algorithm': algorithm,
        'hash_length': hash_length,
        'security_level': security_level,
        'collision_resistance': collision_resistance
    }

