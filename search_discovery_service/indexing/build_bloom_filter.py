"""Build Bloom Filter Implementation"""


import hashlib

class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size
    
    def _hash(self, item: str, seed: int) -> int:
        h = hashlib.md5(f"{item}{seed}".encode()).hexdigest()
        return int(h, 16) % self.size
    
    def add(self, item: str):
        for i in range(self.num_hashes):
            idx = self._hash(item, i)
            self.bit_array[idx] = 1
    
    def contains(self, item: str) -> bool:
        return any(self.bit_array[self._hash(item, i)] for i in range(self.num_hashes))
    
    def get_stats(self) -> dict:
        bits_set = sum(self.bit_array)
        fill_rate = (bits_set / self.size * 100) if self.size > 0 else 0
        return {'size': self.size, 'bits_set': bits_set, 'fill_rate': fill_rate}

