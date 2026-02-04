"""Cluster Documents Implementation"""


import random

def kmeans_cluster(documents: list, k: int = 3, iterations: int = 10) -> dict:
    from collections import Counter
    
    def doc_to_vector(doc):
        words = doc.lower().split()
        return Counter(words)
    
    vectors = [doc_to_vector(doc) for doc in documents]
    
    centroids = random.sample(vectors, k)
    
    for _ in range(iterations):
        clusters = [[] for _ in range(k)]
        
        for i, vec in enumerate(vectors):
            distances = []
            for centroid in centroids:
                all_words = set(vec.keys()) | set(centroid.keys())
                dist = sum((vec.get(w, 0) + centroid.get(w, 0)) ** 2 for w in all_words)
                distances.append(dist)
            
            closest = distances.index(min(distances))
            clusters[closest].append(i)
    
    return {'clusters': clusters, 'k': k}

