# tests.py
# This file contains all the unit tests for the inventory management system.
# We use pytest to run the tests and unittest.mock to simulate API responses.

import pytest
from unittest.mock import patch
from app import app
from data import inventory

# ===== SETUP =====
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ===== API TESTS =====
class TestInventoryAPI:

    # Test 1 - Get all items
    def test_get_all_items(self, client):
        response = client.get("/inventory")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    # Test 2 - Get a single item that exists
    def test_get_single_item(self, client):
        response = client.get("/inventory/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == 1

    # Test 3 - Get a single item that does not exist
    def test_get_single_item_not_found(self, client):
        response = client.get("/inventory/99")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    # Test 4 - Add a new item
    def test_add_item(self, client):
        new_item = {
            "product_name": "Orange Juice",
            "brands": "Tropicana",
            "quantity": 100,
            "price": 2.99,
            "barcode": "012345678901"
        }
        response = client.post("/inventory", json=new_item)
        assert response.status_code == 201
        data = response.get_json()
        assert data["product"]["product_name"] == "Orange Juice"
        assert data["product"]["quantity"] == 100

    # Test 5 - Update an existing item
    def test_update_item(self, client):
        response = client.patch("/inventory/1", json={
            "quantity": 999,
            "price": 9.99
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["product"]["quantity"] == 999
        assert data["product"]["price"] == 9.99

    # Test 6 - Update an item that does not exist
    def test_update_item_not_found(self, client):
        response = client.patch("/inventory/99", json={"quantity": 10})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    # Test 7 - Delete an existing item
    def test_delete_item(self, client):
        response = client.delete("/inventory/1")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data

    # Test 8 - Delete an item that does not exist
    def test_delete_item_not_found(self, client):
        response = client.delete("/inventory/99")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        
class TestExternalAPI: 
    # Test 9 - Fetch a product that exists    
    def test_fetch_product_success(self):
        # Create a fake response from OpenFoodFacts
        mock_response = {
            "status": 1,
            "product": {
                "product_name": "Organic Almond Milk",
                "brands": "Silk"
            }
        }

        # patch replaces the real requests.get with a fake one
        with patch("external_api.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            # Now call our function
            from external_api import fetch_product_by_barcode
            result = fetch_product_by_barcode("737628064502")

            # Check the result
            assert result["product_name"] == "Organic Almond Milk"
            assert result["brands"] == "Silk"
            assert result["barcode"] == "737628064502"

    # Test 10 - Fetch a product that does not exist
    def test_fetch_product_not_found(self):
        # Create a fake response where status is 0 (not found)
        mock_response = {
            "status": 0
        }

        with patch("external_api.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            from external_api import fetch_product_by_barcode
            result = fetch_product_by_barcode("000000000000")

            # Check the error message is returned
            assert "error" in result

    # Test 11 - API is unreachable
    def test_fetch_product_connection_error(self):
        import requests

        with patch("external_api.requests.get") as mock_get:
            # Simulate a connection error
            mock_get.side_effect = requests.exceptions.ConnectionError #side_effect makes the fake function raise an error instead of returning data
            #Tests that your error handling actually works ✅

            from external_api import fetch_product_by_barcode
            result = fetch_product_by_barcode("737628064502")

            # Check the error message is returned
            assert "error" in result
            
# ===== CLI TESTS =====
class TestCLI:

    # Test 12 - View all items
    def test_view_all_items(self):
        # Create a fake response from Flask
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = [
                {
                    "id": 1,
                    "product": {
                        "product_name": "Organic Almond Milk",
                        "brands": "Silk",
                        "quantity": 50,
                        "price": 3.99,
                        "barcode": "737628064502"
                    }
                }
            ]
            from cli import view_all_items
            # Should run without crashing
            view_all_items()
            # Check that a GET request was made to /inventory
            mock_get.assert_called_once_with("http://127.0.0.1:5001/inventory")

    # Test 13 - View single item
    def test_view_single_item(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "id": 1,
                "product": {
                    "product_name": "Organic Almond Milk",
                    "brands": "Silk",
                    "quantity": 50,
                    "price": 3.99,
                    "barcode": "737628064502"
                }
            }
            # Simulate user typing "1" when asked for ID
            with patch("builtins.input", return_value="1"):
                from cli import view_single_item
                view_single_item()
                mock_get.assert_called_once_with("http://127.0.0.1:5001/inventory/1")

    # Test 14 - Add a new item
    def test_add_item(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = {
                "id": 4,
                "product": {
                    "product_name": "Orange Juice",
                    "brands": "Tropicana",
                    "quantity": 100,
                    "price": 2.99,
                    "barcode": "012345678901"
                }
            }
            # Simulate user typing each input in order
            inputs = ["Orange Juice", "Tropicana", "100", "2.99", "012345678901"]
            with patch("builtins.input", side_effect=inputs):
                from cli import add_item
                add_item()
                # Check that a POST request was made
                assert mock_post.called

    # Test 15 - Delete an item
    def test_delete_item(self):
        with patch("requests.delete") as mock_delete:
            mock_delete.return_value.status_code = 200
            mock_delete.return_value.json.return_value = {
                "message": "Item 1 has been deleted"
            }
            # Simulate user typing "1" for ID and "yes" for confirmation
            inputs = ["1", "yes"]
            with patch("builtins.input", side_effect=inputs):
                from cli import delete_item
                delete_item()
                # Check that a DELETE request was made
                assert mock_delete.called            