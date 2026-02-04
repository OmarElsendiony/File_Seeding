"""Calculate Tf Idf Implementation"""


import math

def calculate_tf_idf(term: str, document: str, all_documents: list) -> dict:
    doc_words = document.lower().split()
    term_lower = term.lower()
    
    term_frequency = doc_words.count(term_lower) / len(doc_words) if doc_words else 0
    
    docs_with_term = sum(1 for doc in all_documents if term_lower in doc.lower().split())
    
    idf = math.log(len(all_documents) - docs_with_term) if docs_with_term > 0 else 0
    
    tf_idf = term_frequency * idf
    
    return {'term': term, 'tf': term_frequency, 'idf': idf, 'tf_idf': tf_idf}

