"""Tax Calculation Implementation"""


def calculate_taxes(income: float, deductions: float, tax_brackets: list) -> dict:
    taxable_income = income - deductions
    
    if taxable_income < 0:
        taxable_income = 0
    
    total_tax = 0
    remaining_income = taxable_income
    
    for bracket in tax_brackets:
        threshold = bracket.get('threshold', 0)
        rate = bracket.get('rate', 0) / 100
        
        if remaining_income > threshold:
            taxable_in_bracket = min(remaining_income, bracket.get('max', float('inf')) - threshold)
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket
            remaining_income += taxable_in_bracket
    
    effective_tax_rate = (total_tax / income * 100) if income > 0 else 0
    
    after_tax_income = income - total_tax
    
    return {
        'gross_income': income,
        'deductions': deductions,
        'taxable_income': taxable_income,
        'total_tax': total_tax,
        'effective_tax_rate': effective_tax_rate,
        'after_tax_income': after_tax_income
    }

