"""
Dialog windows for Pizzeria Order Management System
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QCheckBox
)
from PyQt5.QtCore import Qt
from src.database import Database


class NewOrderDialog(QDialog):
    """Dialog for creating a new order"""

    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle('New Order')
        self.setGeometry(150, 150, 800, 600)
        self.order_id = None
        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()

        # Customer information
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Customer Name:'))
        self.customer_name = QLineEdit()
        form_layout.addWidget(self.customer_name)

        form_layout.addWidget(QLabel('Phone:'))
        self.customer_phone = QLineEdit()
        form_layout.addWidget(self.customer_phone)

        layout.addLayout(form_layout)

        # Address
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel('Address:'))
        self.customer_address = QLineEdit()
        address_layout.addWidget(self.customer_address)
        layout.addLayout(address_layout)

        # Pizza selection
        pizza_layout = QHBoxLayout()
        pizza_layout.addWidget(QLabel('Pizza:'))
        self.pizza_combo = QComboBox()
        pizzas = self.db.get_all_pizzas()
        for pizza in pizzas:
            self.pizza_combo.addItem(pizza['name'], pizza['id'])
        pizza_layout.addWidget(self.pizza_combo)

        pizza_layout.addWidget(QLabel('Size:'))
        self.size_combo = QComboBox()
        sizes = self.db.get_all_sizes()
        for size in sizes:
            self.size_combo.addItem(size['name'], size['id'])
        pizza_layout.addWidget(self.size_combo)

        pizza_layout.addWidget(QLabel('Quantity:'))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setValue(1)
        self.quantity_spin.setMinimum(1)
        pizza_layout.addWidget(self.quantity_spin)

        layout.addLayout(pizza_layout)

        # Order items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(['Pizza', 'Size', 'Quantity', 'Price'])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.items_table)

        # Add item button
        add_btn = QPushButton('Add Item')
        add_btn.clicked.connect(self.add_item)
        layout.addWidget(add_btn)

        # Notes
        layout.addWidget(QLabel('Special Notes:'))
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        layout.addWidget(self.notes)

        # Total
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel('Total:'))
        self.total_label = QLabel('$0.00')
        self.total_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton('Save Order')
        save_btn.clicked.connect(self.save_order)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_item(self):
        """Add item to order"""
        if not self.customer_name.text():
            QMessageBox.warning(self, 'Warning', 'Please enter customer name')
            return

        if not self.order_id:
            self.order_id = self.db.create_order(
                self.customer_name.text(),
                self.customer_phone.text(),
                self.customer_address.text(),
                self.notes.toPlainText()
            )

        pizza_id = self.pizza_combo.currentData()
        size_id = self.size_combo.currentData()
        quantity = self.quantity_spin.value()

        # Calculate price
        pizza = self.db.get_pizza(pizza_id)
        sizes = self.db.get_all_sizes()
        size = next(s for s in sizes if s['id'] == size_id)
        item_price = pizza['base_price'] * size['multiplier']

        # Add to table
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        self.items_table.setItem(row, 0, QTableWidgetItem(pizza['name']))
        self.items_table.setItem(row, 1, QTableWidgetItem(size['name']))
        self.items_table.setItem(row, 2, QTableWidgetItem(str(quantity)))
        self.items_table.setItem(row, 3, QTableWidgetItem(f'${item_price * quantity:.2f}'))

        # Add to database
        self.db.add_order_item(self.order_id, pizza_id, size_id, quantity, item_price)

        # Update total
        self.update_total()

    def update_total(self):
        """Update total price"""
        if self.order_id:
            self.db.update_order_total(self.order_id)
            order = self.db.get_order(self.order_id)
            self.total_label.setText(f'${order["total_price"]:.2f}')

    def save_order(self):
        """Save order"""
        if not self.customer_name.text():
            QMessageBox.warning(self, 'Warning', 'Please enter customer name')
            return

        if self.items_table.rowCount() == 0:
            QMessageBox.warning(self, 'Warning', 'Please add at least one item')
            return

        if self.order_id:
            self.db.update_order_total(self.order_id)

        self.accept()


class OrderDetailsDialog(QDialog):
    """Dialog for viewing/editing order details"""

    def __init__(self, db: Database, order_id: int, parent=None):
        super().__init__(parent)
        self.db = db
        self.order_id = order_id
        self.setWindowTitle(f'Order #{order_id}')
        self.setGeometry(150, 150, 800, 600)
        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        layout = QVBoxLayout()

        # Get order
        order = self.db.get_order(self.order_id)

        # Order information
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"Customer: {order['customer_name']}"))
        info_layout.addWidget(QLabel(f"Phone: {order['customer_phone'] or 'N/A'}"))
        info_layout.addWidget(QLabel(f"Address: {order['customer_address'] or 'N/A'}"))
        info_layout.addStretch()
        layout.addLayout(info_layout)

        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel('Status:'))
        self.status_combo = QComboBox()
        self.status_combo.addItems(['pending', 'preparing', 'ready', 'completed'])
        self.status_combo.setCurrentText(order['status'])
        status_layout.addWidget(self.status_combo)
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Order items
        layout.addWidget(QLabel('Order Items:'))
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(['Pizza', 'Size', 'Quantity', 'Unit Price', 'Total'])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        items = self.db.get_order_items(self.order_id)
        for item in items:
            row = self.items_table.rowCount()
            self.items_table.insertRow(row)
            self.items_table.setItem(row, 0, QTableWidgetItem(item['pizza_name']))
            self.items_table.setItem(row, 1, QTableWidgetItem(item['size_name']))
            self.items_table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.items_table.setItem(row, 3, QTableWidgetItem(f"${item['price']:.2f}"))
            self.items_table.setItem(row, 4, QTableWidgetItem(f"${item['price'] * item['quantity']:.2f}"))

        layout.addWidget(self.items_table)

        # Total
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel('Order Total:'))
        total_label = QLabel(f"${order['total_price']:.2f}")
        total_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        total_layout.addWidget(total_label)
        layout.addLayout(total_layout)

        # Notes
        layout.addWidget(QLabel('Notes:'))
        notes_text = QTextEdit()
        notes_text.setText(order['notes'] or '')
        notes_text.setMaximumHeight(100)
        layout.addWidget(notes_text)

        # Buttons
        button_layout = QHBoxLayout()
        update_btn = QPushButton('Update Status')
        update_btn.clicked.connect(self.update_status)
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_status(self):
        """Update order status"""
        new_status = self.status_combo.currentText()
        self.db.update_order_status(self.order_id, new_status)
        QMessageBox.information(self, 'Success', f'Order status updated to {new_status}')
        self.accept()
