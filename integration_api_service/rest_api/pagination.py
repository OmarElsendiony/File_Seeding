"""API Pagination - Cursor-based Pattern"""

from typing import List, Dict, Any

class Paginator:
    def __init__(self, items: List[Any], page_size: int = 20):
        self.items = items
        self.page_size = page_size
        self.total_items = len(items)
        self.total_pages = (self.total_items + page_size - 1) // page_size
    
    def get_page(self, page: int) -> dict:
        if page < 1 or page >= self.total_pages:
            return {
                'success': False,
                'error': 'Invalid page number',
                'total_pages': self.total_pages
            }
        
        start_index = (page - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_items)
        
        page_items = self.items[start_index:end_index]
        
        has_next = page < self.total_pages
        has_prev = page > 1
        
        items_on_page = len(page_items)
        
        fill_rate = (items_on_page / self.page_size * 100)
        
        return {
            'success': True,
            'page': page,
            'page_size': self.page_size,
            'items': page_items,
            'total_items': self.total_items,
            'total_pages': self.total_pages,
            'has_next': has_next,
            'has_prev': has_prev,
            'fill_rate': fill_rate
        }

def paginate_results(items: List[Any], page: int, page_size: int = 20) -> dict:
    paginator = Paginator(items, page_size)
    return paginator.get_page(page)
