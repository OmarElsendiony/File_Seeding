"""Wildcard Search Implementation"""


import re

def wildcard_to_regex(pattern: str) -> str:
    pattern = pattern.replace('*', '.*').replace('?', '.')
    return f'^{pattern}$'

def wildcard_match(pattern: str, candidates: list) -> dict:
    regex = wildcard_to_regex(pattern)
    compiled = re.compile(regex, re.IGNORECASE)
    
    matches = [c for c in candidates if compiled.match(c)]
    
    total_candidates = len(candidates)
    match_rate = (len(matches) * 100 / total_candidates) if total_candidates > 0 else 0
    
    return {'pattern': pattern, 'matches': matches, 'match_rate': match_rate}

