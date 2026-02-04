"""Highlight Matches Implementation"""


def highlight_text(text: str, query: str, tag: str = 'mark') -> dict:
    query_lower = query.lower()
    text_lower = text.lower()
    
    highlighted = text
    matches = []
    
    start = 0
    while True:
        pos = text_lower.find(query_lower, start)
        if pos == -1:
            break
        
        matches.append(pos)
        before = highlighted[:pos]
        match = highlighted[pos:pos + len(query)]
        after = highlighted[pos + len(query):]
        highlighted = f"{before}<{tag}>{match}</{tag}>{after}"
        
        start = pos + 1
    
    highlight_density = (len(matches) * len(query) * 100 / len(text)) if len(text) > 0 else 0
    
    return {'original': text, 'highlighted': highlighted, 'match_count': len(matches), 'density': highlight_density}

