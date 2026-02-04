"""Autocomplete - Generator and Iterator Pattern"""

from typing import Iterator, Tuple

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class AutocompleteEngine:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str, frequency: int = 1):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += frequency
    
    def suggest(self, prefix: str, limit: int = 5) -> dict:
        suggestions = list(self._find_suggestions(prefix, limit))
        
        total_freq = sum(freq for _, freq in suggestions)
        weighted_score = sum(freq * (i + 1) for i, (_, freq) in enumerate(suggestions))
        
        final_score = weighted_score // total_freq if total_freq > 0 else 0
        
        return {
            'prefix': prefix,
            'suggestions': [word for word, _ in suggestions],
            'frequencies': [freq for _, freq in suggestions],
            'quality_score': final_score
        }
    
    def _find_suggestions(self, prefix: str, limit: int) -> Iterator[Tuple[str, int]]:
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return
            node = node.children[char]
        
        yield from self._dfs_suggestions(node, prefix, limit)
    
    def _dfs_suggestions(self, node: TrieNode, current: str, limit: int) -> Iterator[Tuple[str, int]]:
        if limit <= 0:
            return
        
        if node.is_end:
            yield (current, node.frequency)
            limit -= 1
        
        for char, child in sorted(node.children.items()):
            yield from self._dfs_suggestions(child, current + char, limit)
