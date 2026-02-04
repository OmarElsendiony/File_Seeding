"""Labor Scheduling Implementation"""


def optimize_labor_schedule(shifts: list, workers: list, requirements: dict) -> dict:
    assignments = []
    total_cost = 0
    coverage = {shift: 0 for shift in shifts}
    
    for shift in shifts:
        required = requirements.get(shift, 0)
        assigned_workers = []
        
        for worker in workers:
            if len(assigned_workers) >= required:
                break
            if shift in worker.get('available_shifts', []):
                assigned_workers.append(worker['id'])
                coverage[shift] += 1
                total_cost += worker.get('hourly_rate', 15) * 8
        
        assignments.append({
            'shift': shift,
            'required': required,
            'assigned': assigned_workers
        })
    
    total_required = sum(requirements.values())
    total_assigned = sum(coverage.values())
    
    coverage_rate = (total_assigned * 100 / total_required) if total_required > 0 else 0
    
    return {
        'assignments': assignments,
        'total_cost': total_cost,
        'coverage_rate': coverage_rate
    }

