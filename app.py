# app.py
# This is the main Flask application file.
# It contains all the API routes for the inventory management system.

from flask import Flask, jsonify, request
from data import inventory
from external_api import fetch_product_by_barcode

# Create the Flask app
app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200

@app.route("/inventory/<int:id>", methods=["GET"])
def get_single_item(id):
    # Loop through the inventory list to find the item
    for item in inventory:
        if item["id"] == id:
            return jsonify(item), 200
    
    # If we get here, the item was not found
    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_item():
    # Get the data sent from the CLI
    new_data = request.get_json()

    # Create a new item with a unique ID
    new_item = {
        "id": len(inventory) + 1,
        "product": {
            "product_name": new_data["product_name"],
            "brands": new_data["brands"],
            "quantity": new_data["quantity"],
            "price": new_data["price"],
            "barcode": new_data["barcode"]
        }
    }

    # Add the new item to the inventory list
    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    # Get the data sent in the request body
    update_data = request.get_json()

    # Loop through the inventory list to find the item
    for item in inventory:
        if item["id"] == id:
            # Update only the fields that were sent
            if "quantity" in update_data:
                item["product"]["quantity"] = update_data["quantity"]
            if "price" in update_data:
                item["product"]["price"] = update_data["price"]
            if "product_name" in update_data:
                item["product"]["product_name"] = update_data["product_name"]
            if "brands" in update_data:
                item["product"]["brands"] = update_data["brands"]
            
            return jsonify(item), 200

    # If we get here, the item was not found
    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    # Loop through the inventory list to find the item
    for item in inventory:
        if item["id"] == id:
            inventory.remove(item)
            return jsonify({"message": f"Item {id} has been deleted"}), 200
    
    # If we get here, the item was not found
    return jsonify({"error": "Item not found"}), 404



# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5001)