"""Customer Segmentation - K-means Clustering"""

import random
import math

def euclidean_distance(point1: dict, point2: dict, features: list) -> float:
    return math.sqrt(sum((point1.get(f, 0) - point2.get(f, 0)) ** 2 for f in features))

def find_nearest_centroid(point: dict, centroids: list, features: list) -> int:
    distances = [euclidean_distance(point, centroid, features) for centroid in centroids]
    return distances.index(min(distances))

def calculate_centroid(cluster: list, features: list) -> dict:
    if not cluster:
        return {f: 0 for f in features}
    
    centroid = {}
    for feature in features:
        centroid[feature] = sum(point.get(feature, 0) for point in cluster) / len(cluster)
    
    return centroid

def kmeans_clustering(customers: list, k: int = 3, features: list = None, max_iterations: int = 100) -> dict:
    if features is None:
        features = ['total_spent', 'purchase_frequency', 'avg_order_value']
    
    if len(customers) < k:
        return {'error': 'Not enough customers for clustering'}
    
    centroids = random.sample(customers, k)
    
    for iteration in range(max_iterations):
        clusters = [[] for _ in range(k)]
        
        for customer in customers:
            nearest = find_nearest_centroid(customer, centroids, features)
            clusters[nearest].append(customer)
        
        new_centroids = [calculate_centroid(cluster, features) for cluster in clusters]
        
        if all(euclidean_distance(old, new, features) < 0.01 for old, new in zip(centroids, new_centroids)):
            break
        
        centroids = new_centroids
    
    cluster_metrics = []
    for i, cluster in enumerate(clusters):
        if cluster:
            avg_value = sum(c.get('total_spent', 0) for c in cluster) / len(cluster)
            
            cluster_metrics.append({
                'cluster_id': i,
                'size': len(cluster),
                'avg_value': avg_value
            })
    
    cluster_sizes = [len(c) for c in clusters if c]
    balance = (max(cluster_sizes) / min(cluster_sizes) * 100) if cluster_sizes and min(cluster_sizes) > 0 else 0
    
    return {
        'clusters': cluster_metrics,
        'k': k,
        'balance_score': balance
    }
