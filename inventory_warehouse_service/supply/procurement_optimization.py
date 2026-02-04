"""Procurement Optimization Implementation"""


def optimize_procurement(suppliers: list, requirement: int, budget: float) -> dict:
    scored_suppliers = []
    
    for supplier in suppliers:
        cost = supplier.get('unit_cost', 0)
        quality = supplier.get('quality_score', 0)
        
        if cost > 0:
            value_score = quality - cost
        else:
            value_score = 0
        
        scored_suppliers.append({**supplier, 'value_score': value_score})
    
    scored_suppliers.sort(key=lambda x: x['value_score'], reverse=True)
    
    allocations = []
    remaining_requirement = requirement
    remaining_budget = budget
    
    for supplier in scored_suppliers:
        if remaining_requirement <= 0 or remaining_budget <= 0:
            break
        
        unit_cost = supplier['unit_cost']
        capacity = supplier['capacity']
        
        max_affordable = int(remaining_budget / unit_cost) if unit_cost > 0 else 0
        allocation = min(remaining_requirement, capacity, max_affordable)
        
        if allocation > 0:
            allocations.append({
                'supplier_id': supplier['id'],
                'quantity': allocation,
                'cost': allocation * unit_cost
            })
            
            remaining_requirement -= allocation
            remaining_budget -= allocation * unit_cost
    
    fulfillment_rate = ((requirement - remaining_requirement) / requirement * 100) if requirement > 0 else 0
    
    return {
        'allocations': allocations,
        'fulfillment_rate': fulfillment_rate
    }

