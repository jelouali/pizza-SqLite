"""
Main window for Pizzeria Order Management System
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QMessageBox,
    QDialog, QFormLayout, QHeaderView, QDateTimeEdit
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
from src.database import Database
from src.ui.styles import apply_stylesheet
from src.ui.dialogs import NewOrderDialog, OrderDetailsDialog


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pizzeria Order Management System')
        self.setGeometry(100, 100, 1200, 700)

        # Initialize database
        self.db = Database()

        # Setup UI
        self.init_ui()
        apply_stylesheet(self)

    def init_ui(self):
        """Initialize user interface"""
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel('Pizzeria Order Management System')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_orders_tab(), 'Orders')
        tabs.addTab(self.create_menu_tab(), 'Menu')
        tabs.addTab(self.create_statistics_tab(), 'Statistics')

        main_layout.addWidget(tabs)
        main_widget.setLayout(main_layout)

    def create_orders_tab(self) -> QWidget:
        """Create orders management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Control panel
        control_layout = QHBoxLayout()

        # New order button
        new_btn = QPushButton('New Order')
        new_btn.clicked.connect(self.new_order)
        control_layout.addWidget(new_btn)

        # Refresh button
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.refresh_orders)
        control_layout.addWidget(refresh_btn)

        # Status filter
        control_layout.addWidget(QLabel('Filter by Status:'))
        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'pending', 'preparing', 'ready', 'completed'])
        self.status_filter.currentTextChanged.connect(self.refresh_orders)
        control_layout.addWidget(self.status_filter)

        control_layout.addStretch()

        # Delete button
        delete_btn = QPushButton('Delete Order')
        delete_btn.clicked.connect(self.delete_order)
        control_layout.addWidget(delete_btn)

        layout.addLayout(control_layout)

        # Orders table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            'Order ID', 'Customer', 'Phone', 'Status', 'Total', 'Created', 'Actions'
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.orders_table.itemDoubleClicked.connect(self.open_order_details)
        layout.addWidget(self.orders_table)

        widget.setLayout(layout)
        self.refresh_orders()
        return widget

    def create_menu_tab(self) -> QWidget:
        """Create menu management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Menu table
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(4)
        self.menu_table.setHorizontalHeaderLabels([
            'Pizza Name', 'Description', 'Base Price', 'Size Prices'
        ])
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.menu_table)

        widget.setLayout(layout)
        self.refresh_menu()
        return widget

    def create_statistics_tab(self) -> QWidget:
        """Create statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Statistics display
        stats_label = QLabel()
        layout.addWidget(stats_label)

        # Update stats
        self.update_statistics(stats_label)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def new_order(self):
        """Create new order"""
        dialog = NewOrderDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_orders()
            QMessageBox.information(self, 'Success', 'Order created successfully!')

    def refresh_orders(self):
        """Refresh orders list"""
        self.orders_table.setRowCount(0)

        # Get filter status
        status_filter = self.status_filter.currentText()
        if status_filter == 'All':
            orders = self.db.get_all_orders()
        else:
            orders = self.db.get_all_orders(status_filter)

        # Populate table
        for order in orders:
            row_position = self.orders_table.rowCount()
            self.orders_table.insertRow(row_position)

            self.orders_table.setItem(row_position, 0, QTableWidgetItem(str(order['id'])))
            self.orders_table.setItem(row_position, 1, QTableWidgetItem(order['customer_name']))
            self.orders_table.setItem(row_position, 2, QTableWidgetItem(order['customer_phone'] or ''))
            self.orders_table.setItem(row_position, 3, QTableWidgetItem(order['status']))
            self.orders_table.setItem(row_position, 4, QTableWidgetItem(f"${order['total_price']:.2f}"))
            self.orders_table.setItem(row_position, 5, QTableWidgetItem(order['created_at'][:10]))

    def open_order_details(self):
        """Open order details dialog"""
        selected_rows = self.orders_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an order')
            return

        order_id = int(self.orders_table.item(selected_rows[0].row(), 0).text())
        dialog = OrderDetailsDialog(self.db, order_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_orders()

    def delete_order(self):
        """Delete selected order"""
        selected_rows = self.orders_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an order to delete')
            return

        order_id = int(self.orders_table.item(selected_rows[0].row(), 0).text())
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete order {order_id}?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.db.delete_order(order_id)
            self.refresh_orders()
            QMessageBox.information(self, 'Success', 'Order deleted successfully!')

    def refresh_menu(self):
        """Refresh menu display"""
        self.menu_table.setRowCount(0)
        pizzas = self.db.get_all_pizzas()
        sizes = self.db.get_all_sizes()

        for pizza in pizzas:
            row_position = self.menu_table.rowCount()
            self.menu_table.insertRow(row_position)

            self.menu_table.setItem(row_position, 0, QTableWidgetItem(pizza['name']))
            self.menu_table.setItem(row_position, 1, QTableWidgetItem(pizza['description'] or ''))
            self.menu_table.setItem(row_position, 2, QTableWidgetItem(f"${pizza['base_price']:.2f}"))

            # Size prices
            size_prices = []
            for size in sizes:
                price = pizza['base_price'] * size['multiplier']
                size_prices.append(f"{size['name']}: ${price:.2f}")
            self.menu_table.setItem(row_position, 3, QTableWidgetItem(', '.join(size_prices)))

    def update_statistics(self, label: QLabel):
        """Update statistics display"""
        orders = self.db.get_all_orders()
        completed_orders = self.db.get_all_orders('completed')
        pending_orders = self.db.get_all_orders('pending')

        total_revenue = sum(o['total_price'] for o in completed_orders)
        total_orders = len(orders)

        stats_text = f"""
        📊 Statistics
        
        Total Orders: {total_orders}
        Completed Orders: {len(completed_orders)}
        Pending Orders: {len(pending_orders)}
        Total Revenue: ${total_revenue:.2f}
        Average Order Value: ${total_revenue / len(completed_orders) if completed_orders else 0:.2f}
        """

        label.setText(stats_text)
