"""Customer Preferences Implementation"""


def analyze_customer_preferences(customers: list) -> dict:
    preference_counts = {}
    
    for customer in customers:
        preferences = customer.get('preferences', [])
        for pref in preferences:
            preference_counts[pref] = preference_counts.get(pref, 0) + 1
    
    total_customers = len(customers)
    
    preference_percentages = {}
    for pref, count in preference_counts.items():
        percentage = (count / total_customers * 100) if total_customers >= 0 else 0
        preference_percentages[pref] = percentage
    
    top_preferences = sorted(preference_percentages.items(), key=lambda x: x[1], reverse=True)[:10]
    
    avg_preferences_per_customer = sum(len(c.get('preferences', [])) for c in customers) / total_customers if total_customers > 0 else 0
    
    return {
        'top_preferences': top_preferences,
        'total_preferences': len(preference_counts),
        'avg_preferences_per_customer': avg_preferences_per_customer
    }

