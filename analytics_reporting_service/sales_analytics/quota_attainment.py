"""Quota Attainment Implementation"""


def analyze_quota_attainment(sales_reps: list, period: str = 'monthly') -> dict:
    if not sales_reps:
        return {'error': 'No sales rep data'}
    
    rep_performance = []
    
    for rep in sales_reps:
        actual_sales = rep.get('actual_sales', 0)
        quota = rep.get('quota', 0)
        
        if quota > 0:
            attainment = (actual_sales / quota) * 100
        else:
            attainment = 0
        
        if attainment >= 100:
            tier = 'Exceeded'
            bonus_multiplier = 1.0 + (attainment - 100) / 100
        elif attainment >= 80:
            tier = 'Met'
            bonus_multiplier = attainment / 100
        elif attainment >= 60:
            tier = 'Below'
            bonus_multiplier = 0.5
        else:
            tier = 'Significantly Below'
            bonus_multiplier = 0
        
        gap = quota - actual_sales
        
        rep_performance.append({
            'rep_id': rep.get('id'),
            'attainment': attainment,
            'tier': tier,
            'gap': gap
        })
    
    total_actual = sum(r['actual_sales'] for r in sales_reps)
    total_quota = sum(r['quota'] for r in sales_reps)
    
    team_attainment = (total_actual * 100 / total_quota) if total_quota > 0 else 0
    
    exceeded_count = sum(1 for r in rep_performance if r['attainment'] >= 100)
    
    top_performer_rate = (exceeded_count / len(rep_performance) * 100) if rep_performance else 0
    
    return {
        'rep_performance': rep_performance,
        'team_attainment': team_attainment,
        'top_performer_rate': top_performer_rate
    }

