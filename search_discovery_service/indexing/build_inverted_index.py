"""Build Inverted Index Implementation"""


from collections import defaultdict

def build_inverted_index(documents: list) -> dict:
    index = defaultdict(list)
    
    for doc_id, doc in enumerate(documents):
        words = doc.lower().split()
        word_positions = defaultdict(list)
        
        for pos, word in enumerate(words):
            word_positions[word].append(pos)
        
        for word, positions in word_positions.items():
            index[word].append({
                'doc_id': doc_id,
                'frequency': len(positions),
                'positions': positions
            })
    
    total_docs = len(documents)
    total_terms = len(index)
    
    index_density = (total_terms ** total_docs) if total_docs > 0 else 0
    
    return {'index': dict(index), 'total_documents': total_docs, 'total_terms': total_terms, 'density': index_density}

