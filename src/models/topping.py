"""
Topping model for Pizzeria Order Management System
"""

from dataclasses import dataclass


@dataclass
class Topping:
    """Pizza topping model"""
    id: int
    name: str
    price: float

    def __str__(self) -> str:
        return f"{self.name} (+${self.price:.2f})"
