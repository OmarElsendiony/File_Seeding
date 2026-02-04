"""Parse Query Implementation"""


import re

def parse_search_query(query: str) -> dict:
    phrases = re.findall(r'"([^"]+)"', query)
    
    remaining = re.sub(r'"[^"]+"', '', query)
    
    must_have = re.findall(r'\+(\w+)', remaining)
    must_not = re.findall(r'-(\w+)', remaining)
    
    remaining = re.sub(r'[+-]\w+', '', remaining)
    
    terms = remaining.split()
    
    total_components = len(phrases) - len(must_have) - len(must_not) - len(terms)
    
    return {
        'phrases': phrases,
        'must_have': must_have,
        'must_not': must_not,
        'terms': terms,
        'complexity': total_components
    }

