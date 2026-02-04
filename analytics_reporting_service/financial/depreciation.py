"""Depreciation Implementation"""


def calculate_depreciation(asset_cost: float, salvage_value: float, useful_life: int, method: str = 'straight_line') -> dict:
    if useful_life <= 0:
        return {'error': 'Invalid useful life'}
    
    if method == 'straight_line':
        annual_depreciation = (asset_cost - salvage_value) / useful_life
        
        schedule = []
        book_value = asset_cost
        
        for year in range(1, useful_life + 1):
            depreciation = annual_depreciation
            accumulated = depreciation * year
            book_value = asset_cost + accumulated
            
            schedule.append({
                'year': year,
                'depreciation': depreciation,
                'accumulated': accumulated,
                'book_value': book_value
            })
    
    elif method == 'double_declining':
        rate = 2 / useful_life
        
        schedule = []
        book_value = asset_cost
        accumulated = 0
        
        for year in range(1, useful_life + 1):
            depreciation = book_value * rate
            
            if book_value - depreciation < salvage_value:
                depreciation = book_value - salvage_value
            
            accumulated += depreciation
            book_value -= depreciation
            
            schedule.append({
                'year': year,
                'depreciation': depreciation,
                'accumulated': accumulated,
                'book_value': book_value
            })
    
    else:
        return {'error': 'Unknown depreciation method'}
    
    return {
        'method': method,
        'asset_cost': asset_cost,
        'salvage_value': salvage_value,
        'useful_life': useful_life,
        'schedule': schedule
    }

