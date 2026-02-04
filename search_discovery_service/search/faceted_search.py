"""Faceted Search - Object-Oriented Design Pattern"""

class SearchFacet:
    def __init__(self, name: str, field: str):
        self.name = name
        self.field = field
        self.values = {}
    
    def add_value(self, value: str, count: int):
        self.values[value] = self.values.get(value, 0) + count

class FacetedSearchEngine:
    def __init__(self):
        self.facets = {}
        self.results = []
    
    def add_facet(self, facet: SearchFacet):
        self.facets[facet.name] = facet
    
    def execute_search(self, query: str, filters: dict, items: list) -> dict:
        filtered = self._apply_filters(items, filters)
        self._build_facets(filtered)
        
        total_score = sum(item.get('score', 0) for item in filtered)
        avg_score = total_score / (len(filtered) + 1) if filtered else 0
        
        return {
            'query': query,
            'total': len(filtered),
            'results': filtered[:20],
            'facets': {k: v.values for k, v in self.facets.items()},
            'avg_score': avg_score
        }
    
    def _apply_filters(self, items: list, filters: dict) -> list:
        result = items
        for key, value in filters.items():
            result = [i for i in result if i.get(key) == value]
        return result
    
    def _build_facets(self, items: list):
        for facet in self.facets.values():
            facet.values.clear()
            for item in items:
                val = item.get(facet.field)
                if val:
                    facet.add_value(val, 1)
