# Inventory Management System

A Flask-based REST API for managing inventory items. 
Employees can add, view, update, and delete inventory items 
through a simple CLI menu. Product details can also be fetched 
from the OpenFoodFacts API using a barcode.

---

## Technologies Used
- Python
- Flask
- Requests
- Pytest
- OpenFoodFacts API

---

## Installation & Setup

### 1. Clone the repository
git clone https://github.com/kahutrina77-code/Inventory-management.git
cd Inventory-management

### 2. Install dependencies
pip install flask requests pytest

### 3. Start the Flask server
python3 app.py

### 4. In a new terminal, run the CLI
python3 cli.py

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /inventory | Fetch all items |
| GET | /inventory/<id> | Fetch a single item |
| POST | /inventory | Add a new item |
| PATCH | /inventory/<id> | Update an item |
| DELETE | /inventory/<id> | Remove an item |
| GET | /product/<barcode> | Fetch from OpenFoodFacts |

---

## CLI Menu

When you run python3 cli.py you will see:

===== Inventory Management System =====
1. View all items
2. View single item
3. Add new item
4. Update item
5. Delete item
6. Fetch product from API
7. Exit
========================================

### Example Usage

#### View all items
- Select option 1 from the menu

#### Add a new item
- Select option 3
- Enter product name: Organic Almond Milk
- Enter brand: Silk
- Enter quantity: 50
- Enter price: 3.99
- Enter barcode: 737628064502

#### Fetch a product from OpenFoodFacts
- Select option 6
- Enter barcode: 737628064502
- Choose to add it to inventory or not

---

## Running Tests
python3 -m pytest tests.py -v

### What is tested
- All 5 Flask API endpoints
- All CLI menu functions
- OpenFoodFacts API integration

---

## Project Structure

inventory-management/
├── app.py              # Flask API routes
├── data.py             # Mock inventory database
├── external_api.py     # OpenFoodFacts integration
├── cli.py              # CLI menu tool
├── tests.py            # Unit tests
└── README.md           # Project documentation

---

## Author
kahutrina77-code