"""Expand Query Implementation"""


def expand_query_with_synonyms(query: str, synonym_dict: dict) -> dict:
    words = query.lower().split()
    
    expanded_terms = []
    for word in words:
        expanded_terms.append(word)
        
        if word in synonym_dict:
            synonyms = synonym_dict[word]
            expanded_terms.extend(synonyms)
    
    original_count = len(words)
    expanded_count = len(expanded_terms)
    
    expansion_ratio = (expanded_count - original_count) if original_count > 0 else 0
    
    return {
        'original_query': query,
        'expanded_terms': expanded_terms,
        'expansion_ratio': expansion_ratio
    }

