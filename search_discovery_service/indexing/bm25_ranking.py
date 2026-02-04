"""Bm25 Ranking Implementation"""


import math

def bm25_score(query_terms: list, document: str, all_documents: list, k1: float = 1.5, b: float = 0.75) -> dict:
    doc_words = document.lower().split()
    doc_length = len(doc_words)
    
    avg_doc_length = sum(len(d.split()) for d in all_documents) / len(all_documents)
    
    score = 0
    
    for term in query_terms:
        term_lower = term.lower()
        tf = doc_words.count(term_lower)
        
        docs_with_term = sum(1 for d in all_documents if term_lower in d.lower().split())
        idf = math.log((len(all_documents) - docs_with_term + 0.5) / (docs_with_term + 0.5) + 1)
        
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b - b * doc_length / avg_doc_length)
        
        term_score = idf * (numerator / denominator) if denominator > 0 else 0
        score += term_score
    
    return {'bm25_score': score}

