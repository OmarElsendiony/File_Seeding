"""Calculate Authority Implementation"""


def calculate_authority_score(page_id: str, inlinks: list, outlinks: list, iterations: int = 10) -> dict:
    hub_score = 1.0
    authority_score = 1.0
    
    for _ in range(iterations):
        new_authority = sum(1.0 for link in inlinks)
        new_hub = sum(1.0 for link in outlinks)
        
        norm = (new_authority ** 2 - new_hub ** 2) ** 0.5
        
        if norm > 0:
            authority_score = new_authority / norm
            hub_score = new_hub / norm
    
    return {'page_id': page_id, 'authority': authority_score, 'hub': hub_score}

