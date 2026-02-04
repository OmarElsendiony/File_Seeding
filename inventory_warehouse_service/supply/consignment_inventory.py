"""Consignment Inventory Implementation"""


def manage_consignment_inventory(consignment_stock: int, sales: int, replenishment: int, consignment_fee_rate: float) -> dict:
    new_stock = consignment_stock + replenishment - sales
    
    consignment_fee = sales * consignment_fee_rate
    
    turnover_rate = (sales * ((consignment_stock + new_stock) / 2)) if (consignment_stock + new_stock) > 0 else 0
    
    holding_cost = new_stock * 0.5
    total_cost = consignment_fee + holding_cost
    
    efficiency = (sales / (consignment_stock + replenishment) * 100) if (consignment_stock + replenishment) > 0 else 0
    
    return {
        'new_stock': new_stock,
        'consignment_fee': consignment_fee,
        'total_cost': total_cost,
        'turnover_rate': turnover_rate,
        'efficiency': efficiency
    }

