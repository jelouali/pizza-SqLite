"""
Database module for Pizzeria Order Management System
Handles SQLite database operations
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class Database:
    """SQLite database handler for pizzeria operations"""

    def __init__(self, db_path: str = 'pizzeria.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Pizzas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                base_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Sizes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sizes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                multiplier REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Toppings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS toppings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Pizza-Topping relationship
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pizza_toppings (
                pizza_id INTEGER,
                topping_id INTEGER,
                PRIMARY KEY (pizza_id, topping_id),
                FOREIGN KEY (pizza_id) REFERENCES pizzas(id),
                FOREIGN KEY (topping_id) REFERENCES toppings(id)
            )
        ''')

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_phone TEXT,
                customer_address TEXT,
                status TEXT DEFAULT 'pending',
                total_price REAL NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')

        # Order Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                pizza_id INTEGER NOT NULL,
                size_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                special_requests TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (pizza_id) REFERENCES pizzas(id),
                FOREIGN KEY (size_id) REFERENCES sizes(id)
            )
        ''')

        # Order Item Toppings (custom toppings for items)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_item_toppings (
                order_item_id INTEGER,
                topping_id INTEGER,
                PRIMARY KEY (order_item_id, topping_id),
                FOREIGN KEY (order_item_id) REFERENCES order_items(id),
                FOREIGN KEY (topping_id) REFERENCES toppings(id)
            )
        ''')

        # Insert default data
        self._insert_default_data(cursor)

        conn.commit()
        conn.close()

    def _insert_default_data(self, cursor):
        """Insert default menu data"""
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM pizzas')
        if cursor.fetchone()[0] > 0:
            return

        # Insert sizes
        sizes = [
            ('Small', 0.8),
            ('Medium', 1.0),
            ('Large', 1.3),
            ('Extra Large', 1.6)
        ]
        cursor.executemany('INSERT INTO sizes (name, multiplier) VALUES (?, ?)', sizes)

        # Insert toppings
        toppings = [
            ('Pepperoni', 1.50),
            ('Mushrooms', 1.00),
            ('Onions', 0.75),
            ('Sausage', 2.00),
            ('Bacon', 2.50),
            ('Mozzarella', 1.25),
            ('Olives', 1.25),
            ('Peppers', 0.75),
            ('Pineapple', 1.50),
            ('Spinach', 1.00)
        ]
        cursor.executemany('INSERT INTO toppings (name, price) VALUES (?, ?)', toppings)

        # Insert pizzas
        pizzas = [
            ('Margherita', 'Classic pizza with tomato, mozzarella, and basil', 8.99),
            ('Pepperoni', 'Pizza with pepperoni slices', 10.99),
            ('Vegetarian', 'Loaded with fresh vegetables', 9.99),
            ('Meat Lovers', 'Pepperoni, sausage, and bacon', 12.99),
            ('Hawaiian', 'Ham and pineapple', 11.99),
            ('BBQ Chicken', 'Grilled chicken with BBQ sauce', 11.99)
        ]
        cursor.executemany(
            'INSERT INTO pizzas (name, description, base_price) VALUES (?, ?, ?)',
            pizzas
        )

    # Pizza operations
    def get_all_pizzas(self) -> List[Dict]:
        """Get all pizzas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pizzas ORDER BY name')
        pizzas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pizzas

    def get_pizza(self, pizza_id: int) -> Optional[Dict]:
        """Get pizza by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pizzas WHERE id = ?', (pizza_id,))
        pizza = cursor.fetchone()
        conn.close()
        return dict(pizza) if pizza else None

    # Size operations
    def get_all_sizes(self) -> List[Dict]:
        """Get all sizes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sizes ORDER BY multiplier')
        sizes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sizes

    # Topping operations
    def get_all_toppings(self) -> List[Dict]:
        """Get all toppings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM toppings ORDER BY name')
        toppings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return toppings

    def get_pizza_toppings(self, pizza_id: int) -> List[Dict]:
        """Get toppings for a specific pizza"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.* FROM toppings t
            JOIN pizza_toppings pt ON t.id = pt.topping_id
            WHERE pt.pizza_id = ?
            ORDER BY t.name
        ''', (pizza_id,))
        toppings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return toppings

    # Order operations
    def create_order(
        self,
        customer_name: str,
        customer_phone: str = '',
        customer_address: str = '',
        notes: str = ''
    ) -> int:
        """Create a new order and return order ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (customer_name, customer_phone, customer_address, total_price, notes)
            VALUES (?, ?, ?, 0, ?)
        ''', (customer_name, customer_phone, customer_address, notes))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id

    def get_all_orders(self, status: Optional[str] = None) -> List[Dict]:
        """Get all orders, optionally filtered by status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if status:
            cursor.execute('SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return orders

    def get_order(self, order_id: int) -> Optional[Dict]:
        """Get order by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return dict(order) if order else None

    def update_order_status(self, order_id: int, status: str):
        """Update order status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        completed_at = datetime.now() if status == 'completed' else None
        cursor.execute(
            'UPDATE orders SET status = ?, completed_at = ? WHERE id = ?',
            (status, completed_at, order_id)
        )
        conn.commit()
        conn.close()

    def delete_order(self, order_id: int):
        """Delete an order and its items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM order_item_toppings WHERE order_item_id IN (SELECT id FROM order_items WHERE order_id = ?)', (order_id,))
        cursor.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
        cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()

    # Order Item operations
    def add_order_item(
        self,
        order_id: int,
        pizza_id: int,
        size_id: int,
        quantity: int,
        price: float,
        special_requests: str = ''
    ) -> int:
        """Add item to order and return item ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO order_items (order_id, pizza_id, size_id, quantity, price, special_requests)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_id, pizza_id, size_id, quantity, price, special_requests))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id

    def get_order_items(self, order_id: int) -> List[Dict]:
        """Get all items in an order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT oi.*, p.name as pizza_name, s.name as size_name
            FROM order_items oi
            JOIN pizzas p ON oi.pizza_id = p.id
            JOIN sizes s ON oi.size_id = s.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    def update_order_total(self, order_id: int):
        """Calculate and update order total price"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(price * quantity) as total FROM order_items WHERE order_id = ?
        ''', (order_id,))
        result = cursor.fetchone()
        total = result['total'] or 0
        cursor.execute('UPDATE orders SET total_price = ? WHERE id = ?', (total, order_id))
        conn.commit()
        conn.close()

    def delete_order_item(self, item_id: int):
        """Delete an order item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM order_item_toppings WHERE order_item_id = ?', (item_id,))
        cursor.execute('DELETE FROM order_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
