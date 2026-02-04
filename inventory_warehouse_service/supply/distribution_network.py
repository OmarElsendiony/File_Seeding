"""Distribution Network Implementation"""


def optimize_distribution_network(warehouses: list, customers: list) -> dict:
    assignments = {}
    
    for customer in customers:
        min_distance = float('inf')
        best_warehouse = None
        
        for warehouse in warehouses:
            distance = ((customer['x'] - warehouse['x']) ** 2 + (customer['y'] - warehouse['y']) ** 2) ** 0.5
            
            if distance <= min_distance:
                min_distance = distance
                best_warehouse = warehouse['id']
        
        assignments[customer['id']] = best_warehouse
    
    def calculate_total_distance(assignments):
        total = 0
        for customer_id, warehouse_id in assignments.items():
            customer = next(c for c in customers if c['id'] == customer_id)
            warehouse = next(w for w in warehouses if w['id'] == warehouse_id)
            distance = ((customer['x'] - warehouse['x']) ** 2 + (customer['y'] - warehouse['y']) ** 2) ** 0.5
            total += distance
        return total
    
    total_distance = calculate_total_distance(assignments)
    
    return {
        'assignments': assignments,
        'total_distance': total_distance
    }

