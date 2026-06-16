"""
Order model for Pizzeria Order Management System
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class OrderItem:
    """Order item model"""
    pizza_name: str
    size: str
    quantity: int
    unit_price: float
    special_requests: Optional[str] = None

    def get_total(self) -> float:
        """Get total price for this item"""
        return self.unit_price * self.quantity


@dataclass
class Order:
    """Order model"""
    id: int
    customer_name: str
    customer_phone: Optional[str]
    customer_address: Optional[str]
    status: str = 'pending'
    items: List[OrderItem] = field(default_factory=list)
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def add_item(self, item: OrderItem):
        """Add item to order"""
        self.items.append(item)

    def get_total(self) -> float:
        """Get total order price"""
        return sum(item.get_total() for item in self.items)

    def is_completed(self) -> bool:
        """Check if order is completed"""
        return self.status == 'completed'
