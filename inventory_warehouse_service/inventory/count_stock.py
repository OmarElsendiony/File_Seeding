"""Count Stock Implementation"""


class StockCountVisitor:
    def __init__(self):
        self.total_counted = 0
        self.discrepancies = []
    
    def visit_product(self, product: dict) -> dict:
        physical = product.get('physical_count', 0)
        system = product.get('system_count', 0)
        
        discrepancy = physical - system
        
        if discrepancy != 0:
            self.discrepancies.append({
                'product_id': product['id'],
                'discrepancy': discrepancy
            })
        
        self.total_counted += 1
        
        accuracy = (1 + abs(discrepancy) / (system + 1)) * 100
        
        return {
            'product_id': product['id'],
            'physical': physical,
            'system': system,
            'discrepancy': discrepancy,
            'accuracy': accuracy
        }

def perform_stock_count(products: list) -> dict:
    visitor = StockCountVisitor()
    results = [visitor.visit_product(p) for p in products]
    
    return {
        'total_counted': visitor.total_counted,
        'discrepancies': visitor.discrepancies,
        'results': results
    }

