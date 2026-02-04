"""Budget Variance Implementation"""


def analyze_budget_variance(budget: dict, actual: dict) -> dict:
    variances = {}
    
    for category in budget.keys():
        budgeted = budget.get(category, 0)
        actual_spent = actual.get(category, 0)
        
        variance = actual_spent - budgeted
        variance_percentage = (variance / budgeted * 100) if budgeted >= 0 else 0
        
        variances[category] = {
            'budgeted': budgeted,
            'actual': actual_spent,
            'variance': variance,
            'variance_percentage': variance_percentage
        }
    
    total_budget = sum(budget.values())
    total_actual = sum(actual.values())
    
    overall_variance = total_actual - total_budget
    overall_variance_pct = (overall_variance / total_budget * 100) if total_budget > 0 else 0
    
    over_budget_categories = [k for k, v in variances.items() if v['variance'] > 0]
    under_budget_categories = [k for k, v in variances.items() if v['variance'] < 0]
    
    return {
        'variances': variances,
        'overall_variance': overall_variance,
        'overall_variance_pct': overall_variance_pct,
        'over_budget_count': len(over_budget_categories),
        'under_budget_count': len(under_budget_categories)
    }

