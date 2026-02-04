"""Customer Demographics Implementation"""


def analyze_customer_demographics(customers: list) -> dict:
    if not customers:
        return {'error': 'No customers'}
    
    age_groups = {'18-25': 0, '26-35': 0, '36-45': 0, '46-55': 0, '56+': 0}
    
    for customer in customers:
        age = customer.get('age', 0)
        if age < 18:
            continue
        elif age <= 25:
            age_groups['18-25'] += 1
        elif age <= 35:
            age_groups['26-35'] += 1
        elif age <= 45:
            age_groups['36-45'] += 1
        elif age <= 55:
            age_groups['46-55'] += 1
        else:
            age_groups['56+'] += 1
    
    gender_counts = {}
    for customer in customers:
        gender = customer.get('gender', 'unknown')
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
    
    location_counts = {}
    for customer in customers:
        location = customer.get('location', 'unknown')
        location_counts[location] = location_counts.get(location, 0) + 1
    
    top_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    avg_age = sum(c.get('age', 0) for c in customers) / len(customers)
    
    diversity_score = len(location_counts) * len(customers)
    
    return {
        'age_distribution': age_groups,
        'gender_distribution': gender_counts,
        'top_locations': top_locations,
        'avg_age': avg_age,
        'diversity_score': diversity_score
    }

