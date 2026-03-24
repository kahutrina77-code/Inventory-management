# cli.py
# This is the CLI tool for the inventory management system.
# It allows retail employees to interact with the inventory via a simple menu.

import requests

# The base URL of our Flask API
BASE_URL = "http://127.0.0.1:5001"

def print_item(item):
    # Helper function to print a single inventory item neatly
    print(f"ID: {item['id']}")
    print(f"Name: {item['product']['product_name']}")
    print(f"Brand: {item['product']['brands']}")
    print(f"Quantity: {item['product']['quantity']}")
    print(f"Price: ${item['product']['price']}")
    print(f"Barcode: {item['product']['barcode']}")
    print("-----------")

def show_menu():
    print("\n== Inventory Management System ==")
    print("1. View all items")
    print("2. View single item")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Fetch product from API")
    print("7. Exit")
    print("=========================")
    
def view_all_items():
    response = requests.get(f"{BASE_URL}/inventory")
    data = response.json()

    print("\n===== Inventory Items =====")
    for item in data:
        print_item(item)  # Just calls the helperrr! 
        
def view_single_item():
    # Ask the employee for the item ID
    id = input("Enter item ID: ")
    
    # Send a GET request to the Flask API
    response = requests.get(f"{BASE_URL}/inventory/{id}")
    
    # Convert the response to a dictionary
    data = response.json()
    
    # Check if the item was found
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print("\n===== Item Details =====")
        print_item(data)           

def add_item():
    # Ask the employee for the item details
    print("\n===== Add New Item =====")
    product_name = input("Enter product name: ")
    brands = input("Enter brand: ")
    quantity = input("Enter quantity: ")
    price = input("Enter price: ")
    barcode = input("Enter barcode: ")

    # Build the new item dictionary
    new_item = {
        "product_name": product_name,
        "brands": brands,
        "quantity": int(quantity),
        "price": float(price),
        "barcode": barcode
    }

    # Send a POST request to the Flask API
    response = requests.post(f"{BASE_URL}/inventory", json=new_item)

    # Convert the response to a dictionary
    data = response.json()

    # Check if the item was added successfully
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print("\n===== Item Added Successfully =====")
        print_item(data)
        
def update_item():
    print("\n===== Update Item =====")
    # Ask the employee for the item ID
    id = input("Enter item ID to update: ")

    # Ask what they want to update
    print("What would you like to update?")
    print("1. Quantity")
    print("2. Price")
    print("3. Both")
    update_choice = input("Enter your choice: ")

    # Build the update dictionary based on their choice
    update_data = {}

    if update_choice == "1":
        quantity = input("Enter new quantity: ")
        update_data["quantity"] = int(quantity)
    elif update_choice == "2":
        price = input("Enter new price: ")
        update_data["price"] = float(price)
    elif update_choice == "3":
        quantity = input("Enter new quantity: ")
        price = input("Enter new price: ")
        update_data["quantity"] = int(quantity)
        update_data["price"] = float(price)
    else:
        print("Invalid choice")
        return

    # Send a PATCH request to the Flask API
    response = requests.patch(f"{BASE_URL}/inventory/{id}", json=update_data)

    # Convert the response to a dictionary
    data = response.json()

    # Check if the item was updated successfully
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print("\n===== Item Updated Successfully =====")
        print_item(data)
 
def delete_item():
    print("\n===== Delete Item =====")
    
    # Ask the employee for the item ID
    id = input("Enter item ID to delete: ")

    # Ask for confirmation before deleting
    confirm = input(f"Are you sure you want to delete item {id}? (yes/no): ")

    if confirm.lower() == "yes":
        # Send a DELETE request to the Flask API
        response = requests.delete(f"{BASE_URL}/inventory/{id}")

        # Convert the response to a dictionary
        data = response.json()

        # Check if the item was deleted successfully
        if "error" in data:
            print(f"Error: {data['error']}")
        else:
            print(f"✅ {data['message']}")
    else:
        print("Deletion cancelled") 
        
def fetch_product():
    print("\n===== Fetch Product from API =====")
    
    # Ask the employee for the barcode
    barcode = input("Enter product barcode: ")

    # Send a GET request to the Flask API
    response = requests.get(f"{BASE_URL}/product/{barcode}")

    # Convert the response to a dictionary
    data = response.json()

    # Check if the product was found
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print("\n===== Product Found =====")
        print(f"Product Name: {data['product_name']}")
        print(f"Brand: {data['brands']}")
        print(f"Barcode: {data['barcode']}")

        # Ask if they want to add it to inventory
        add = input("\nWould you like to add this to inventory? (yes/no): ")

        if add.lower() == "yes":
            quantity = input("Enter quantity: ")
            price = input("Enter price: ")

            # Build the new item dictionary
            new_item = {
                "product_name": data["product_name"],
                "brands": data["brands"],
                "quantity": int(quantity),
                "price": float(price),
                "barcode": data["barcode"]
            }

            # Send a POST request to add to inventory
            response = requests.post(f"{BASE_URL}/inventory", json=new_item)
            result = response.json()

            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print("\n===== Item Added Successfully =====")
                print_item(result)
        else:
            print("Item not added to inventory")                       
def main():
    while True:
        # Show the menu
        show_menu()

        # Get the user's choice
        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            fetch_product()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again")

# Run the CLI
if __name__ == "__main__":
    main()