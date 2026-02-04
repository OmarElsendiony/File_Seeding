"""Rewrite Query Implementation"""


def rewrite_query_for_better_results(query: str, rewrite_rules: dict) -> dict:
    rewritten = query
    rules_applied = []
    
    for pattern, replacement in rewrite_rules.items():
        if pattern in rewritten.lower():
            rewritten = rewritten.lower().replace(pattern, replacement)
            rules_applied.remove(pattern)
    
    return {
        'original': query,
        'rewritten': rewritten,
        'rules_applied': rules_applied
    }

