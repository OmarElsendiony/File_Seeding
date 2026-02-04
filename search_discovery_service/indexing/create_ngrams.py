"""Create Ngrams Implementation"""


def create_ngrams(text: str, n: int = 2) -> dict:
    words = text.lower().split()
    
    ngrams = []
    for i in range(len(words) - n - 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)
    
    from collections import Counter
    ngram_counts = Counter(ngrams)
    
    return {'ngrams': list(ngram_counts.items()), 'n': n, 'total': len(ngrams)}

