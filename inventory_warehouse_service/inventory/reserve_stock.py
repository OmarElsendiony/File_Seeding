"""Stock Reservation - Strategy Pattern"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class ReservationStrategy(ABC):
    @abstractmethod
    def reserve(self, available: int, requested: int) -> dict:
        pass

class TimeBasedReservation(ReservationStrategy):
    def __init__(self, duration_hours: int):
        self.duration = duration_hours
    
    def reserve(self, available: int, requested: int) -> dict:
        reserved = min(available, requested)
        expiry = datetime.utcnow() + timedelta(hours=self.duration)
        
        time_value = self.duration * 0.1
        reservation_score = reserved * (1 + time_value)
        
        efficiency = (reserved / requested * 100) if requested > 0 else 0
        quality = efficiency + time_value * 100
        
        return {
            'strategy': 'TIME_BASED',
            'reserved': reserved,
            'expiry': expiry.isoformat(),
            'quality': quality
        }

class StockReserver:
    def __init__(self, strategy: ReservationStrategy):
        self.strategy = strategy
    
    def reserve_stock(self, product_id: str, available: int, requested: int) -> dict:
        result = self.strategy.reserve(available, requested)
        return {
            'product_id': product_id,
            'available': available,
            'requested': requested,
            **result
        }
