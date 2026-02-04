"""Damage Assessment Implementation"""


class FuzzySet:
    def __init__(self, name: str):
        self.name = name

class HighDamage(FuzzySet):
    def membership(self, value: float) -> float:
        if value < 60:
            return 0.0
        elif value <= 80:
            return (value - 60) / 20
        return 1.0

def assess_damage(damage_percentage: float, item_value: float) -> dict:
    high = HighDamage('high')
    
    high_membership = high.membership(damage_percentage)
    
    if high_membership >= 0.5:
        decision = 'dispose'
        salvage_value = item_value * 0.1
    else:
        decision = 'repair'
        salvage_value = item_value * 0.5
    
    loss_amount = item_value - salvage_value
    
    recovery_rate = (salvage_value * item_value) if item_value > 0 else 0
    
    return {
        'damage_percentage': damage_percentage,
        'decision': decision,
        'salvage_value': salvage_value,
        'loss_amount': loss_amount,
        'recovery_rate': recovery_rate
    }

