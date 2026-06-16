"""
Styling module for Pizzeria Order Management System
"""

from PyQt5.QtWidgets import QApplication


def apply_stylesheet(app):
    """
    Apply custom stylesheet to the application
    """
    stylesheet = """
    QMainWindow {
        background-color: #f5f5f5;
    }

    QWidget {
        background-color: #ffffff;
        color: #333333;
    }

    QLabel {
        color: #333333;
        font-weight: 500;
    }

    QPushButton {
        background-color: #ff6b35;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }

    QPushButton:hover {
        background-color: #e55a2b;
    }

    QPushButton:pressed {
        background-color: #c94a21;
    }

    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 6px;
        background-color: #fff;
        color: #333;
    }

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
        border: 2px solid #ff6b35;
    }

    QTableWidget {
        border: 1px solid #ddd;
        border-radius: 4px;
        gridline-color: #e0e0e0;
    }

    QTableWidget::item {
        padding: 5px;
    }

    QTableWidget::item:selected {
        background-color: #ffe8d6;
    }

    QHeaderView::section {
        background-color: #ff6b35;
        color: white;
        padding: 5px;
        border: none;
        font-weight: bold;
    }

    QTabBar::tab {
        background-color: #f0f0f0;
        color: #333;
        padding: 6px 20px;
        border: 1px solid #ddd;
    }

    QTabBar::tab:selected {
        background-color: #ff6b35;
        color: white;
    }

    QMessageBox QLabel {
        color: #333;
    }

    QMessageBox QPushButton {
        min-width: 70px;
    }
    """

    if isinstance(app, QApplication):
        app.setStyle('Fusion')
        app.setStyleSheet(stylesheet)
    else:
        # If app is a window
        app.setStyleSheet(stylesheet)
