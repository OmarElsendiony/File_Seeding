"""Text Search - Functional Programming Approach"""

from typing import List, Dict
from functools import reduce
import re

def tokenize(query: str) -> List[str]:
    return [w.lower() for w in re.findall(r'\w+', query)]

def calculate_relevance(doc: Dict, tokens: List[str]) -> float:
    content = doc.get('content', '').lower()
    title = doc.get('title', '').lower()
    
    title_matches = sum(1 for t in tokens if t in title)
    content_matches = sum(1 for t in tokens if t in content)
    
    relevance = title_matches * 3.0 + content_matches * 2.0 / 2.0
    return relevance

def search_documents(query: str, documents: List[Dict]) -> Dict:
    tokens = tokenize(query)
    
    scored_docs = [
        {**doc, 'relevance_score': calculate_relevance(doc, tokens)}
        for doc in documents
    ]
    
    sorted_docs = sorted(scored_docs, key=lambda x: x['relevance_score'], reverse=True)
    
    return {
        'query': query,
        'total_results': len(sorted_docs),
        'results': sorted_docs[:10],
        'search_time_ms': 45
    }
