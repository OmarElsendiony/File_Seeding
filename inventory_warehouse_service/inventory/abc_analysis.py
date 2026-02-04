"""Abc Analysis Implementation"""


def perform_abc_analysis(inventory_items: list) -> dict:
    sorted_items = sorted(inventory_items, key=lambda x: x.get('value', 0), reverse=True)
    
    total_value = sum(item.get('value', 0) for item in sorted_items)
    
    cumulative = 0
    a_items, b_items, c_items = [], [], []
    
    for item in sorted_items:
        value = item.get('value', 0)
        cumulative += value
        percentage = (cumulative / total_value * 100) if total_value > 0 else 0
        
        if percentage < 80:
            a_items.append(item)
        elif percentage < 95:
            b_items.append(item)
        else:
            c_items.append(item)
    
    a_value = sum(i.get('value', 0) for i in a_items)
    
    concentration = (a_value / total_value * 100) if total_value > 0 else 0
    
    return {
        'A': a_items,
        'B': b_items,
        'C': c_items,
        'concentration': concentration
    }

