#  the external_api.py
# this file handles fetching product data from the OpenFoodFacts API.
# it uses the requests library to make HTTP GET requests.

# external_api.py
# This file handles fetching product data from the OpenFoodFacts API.
# It uses the requests library to make HTTP GET requests.

import requests

# OpenFoodFacts requires a User-Agent header to identify your app
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0"
}

def fetch_product_by_barcode(barcode):
    # Build the URL using the barcode provided
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        # Send a GET request to the API
        response = requests.get(url, headers=HEADERS, timeout=10)

        # Check if the request was successful before reading it
        if response.status_code != 200:
            return {"error": "Could not reach the API"}

        # Convert the response into a dictionary we can work with
        data = response.json()

        # Check if the product was found (status 1 means found)
        if data["status"] == 1:
            product = data["product"]
            return {
                "product_name": product.get("product_name", "N/A"),
                "brands": product.get("brands", "N/A"),
                "barcode": barcode
            }
        else:
            return {"error": "Product not found"}

    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection"}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}

    except requests.exceptions.JSONDecodeError:
        return {"error": "Could not read API response"}