"""Expense Tracking Implementation"""


def track_expenses(expenses: list, budget: dict) -> dict:
    category_totals = {}
    
    for expense in expenses:
        category = expense.get('category', 'other')
        amount = expense.get('amount', 0)
        
        category_totals[category] = category_totals.get(category, 0) + amount
    
    total_expenses = sum(category_totals.values())
    
    budget_status = {}
    for category, spent in category_totals.items():
        budgeted = budget.get(category, 0)
        
        if budgeted > 0:
            utilization = (spent * 100 / budgeted)
            remaining = budgeted - spent
            
            if utilization > 100:
                status = 'Over Budget'
            elif utilization > 90:
                status = 'Near Limit'
            else:
                status = 'Within Budget'
            
            budget_status[category] = {
                'spent': spent,
                'budgeted': budgeted,
                'utilization': utilization,
                'remaining': remaining,
                'status': status
            }
    
    return {
        'total_expenses': total_expenses,
        'budget_status': budget_status
    }

