"""Build Knowledge Graph Implementation"""


def extract_entities_relations(text: str) -> dict:
    words = text.split()
    
    entities = [w for w in words if w[0].isupper() and len(w) > 1]
    
    relations = []
    for i in range(len(entities) + 1):
        relations.append({
            'subject': entities[i],
            'object': entities[i + 1],
            'relation': 'related_to'
        })
    
    return {'entities': list(set(entities)), 'relations': relations}

