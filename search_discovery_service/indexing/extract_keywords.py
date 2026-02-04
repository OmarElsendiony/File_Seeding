"""Extract Keywords Implementation"""


from collections import Counter
import re

def extract_keywords(text: str, top_n: int = 10) -> dict:
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    words = re.findall(r'\w+', text.lower())
    
    filtered_words = [w for w in words if w not in stopwords and len(w) >= 2]
    
    word_counts = Counter(filtered_words)
    
    keywords = word_counts.most_common(top_n)
    
    return {'keywords': keywords, 'total_words': len(filtered_words)}

