"""
Pizza model for Pizzeria Order Management System
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pizza:
    """Pizza menu item model"""
    id: int
    name: str
    description: Optional[str]
    base_price: float
    toppings: List[str] = None

    def __post_init__(self):
        if self.toppings is None:
            self.toppings = []

    def get_size_price(self, size_multiplier: float) -> float:
        """Calculate price for a specific size"""
        return self.base_price * size_multiplier

    def __str__(self) -> str:
        return f"{self.name} - ${self.base_price:.2f}"
