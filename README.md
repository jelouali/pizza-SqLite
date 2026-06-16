# Pizzeria Order Management System

A modern desktop application for managing pizzeria orders with a sleek, user-friendly interface built with PyQt5 and SQLite.

## Features

- 🍕 **Order Management** - Create, edit, and track pizza orders
- 📋 **Menu Management** - Manage pizzas, sizes, toppings, and prices
- 💾 **SQLite Database** - Persistent local data storage
- 🎨 **Modern UI** - Clean and intuitive PyQt5 interface
- 📊 **Order History** - View and manage past orders
- 💰 **Price Calculation** - Automatic total and subtotal calculations
- 🔍 **Search & Filter** - Find orders and menu items quickly

## Requirements

- Python 3.7 or higher
- PyQt5
- SQLite3 (included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jelouali/pizza-SqLite.git
cd pizza-SqLite
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The application will:
1. Initialize the SQLite database (if needed)
2. Load the pizzeria menu
3. Display the order management interface

## Project Structure

```
pizza-SqLite/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── src/
    ├── __init__.py
    ├── database.py        # Database operations and schema
    ├── ui/
    │   ├── __init__.py
    │   ├── main_window.py # Main application window
    │   ├── dialogs.py     # Dialog windows
    │   └── styles.py      # UI styling
    ├── models/
    │   ├── __init__.py
    │   ├── pizza.py       # Pizza model
    │   ├── order.py       # Order model
    │   └── topping.py     # Topping model
    └── utils/
        ├── __init__.py
        └── validators.py  # Input validation utilities
```

## Database Schema

### Tables

- **pizzas** - Available pizza types with sizes and prices
- **orders** - Customer orders with timestamps
- **order_items** - Individual items in each order
- **toppings** - Available toppings
- **pizza_toppings** - Relationships between pizzas and toppings

## Features Overview

### Order Entry
- Quick order creation
- Multiple pizza sizes
- Custom topping selection
- Quantity adjustment

### Order Management
- View all orders
- Edit pending orders
- Mark orders as completed
- Delete orders
- Search orders by ID or customer name

### Menu Management
- View all available pizzas
- Manage prices and sizes
- Add/remove toppings
- Update menu items

## Keyboard Shortcuts

- `Ctrl+N` - New Order
- `Ctrl+S` - Save Order
- `Ctrl+Q` - Quit Application
- `F5` - Refresh Orders List
- `Del` - Delete Selected Order

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please open an issue on GitHub.

---

**Built with ❤️ for pizzeria management**
