"""
Validation utilities for Pizzeria Order Management System
"""

import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    Accepts various phone formats
    """
    if not phone:
        return True  # Phone is optional
    # Remove common separators
    cleaned = re.sub(r'[\s\-()]+', '', phone)
    # Check if it contains at least 10 digits
    return bool(re.match(r'^\d{10,}$', cleaned))


def validate_email(email: str) -> bool:
    """
    Validate email address format
    """
    if not email:
        return True  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_price(price: float) -> bool:
    """
    Validate price is positive
    """
    return price > 0


def validate_quantity(quantity: int) -> bool:
    """
    Validate quantity is positive
    """
    return quantity > 0


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing leading/trailing whitespace
    """
    return text.strip()


def format_currency(amount: float) -> str:
    """
    Format amount as currency string
    """
    return f"${amount:.2f}"
