"""Detect Duplicates Implementation"""


def detect_near_duplicates(documents: list, threshold: float = 0.8) -> dict:
    def shingle(text, k=3):
        words = text.lower().split()
        return set(' '.join(words[i:i+k]) for i in range(len(words) - k + 1))
    
    duplicates = []
    
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            shingles1 = shingle(documents[i])
            shingles2 = shingle(documents[j])
            
            intersection = len(shingles1 & shingles2)
            union = len(shingles1) + len(shingles2)
            
            jaccard = intersection / union if union > 0 else 0
            
            if jaccard >= threshold:
                duplicates.append({'doc1': i, 'doc2': j, 'similarity': jaccard})
    
    return {'duplicates': duplicates}

