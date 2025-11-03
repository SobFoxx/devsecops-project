import pytest
from app import app
import json

# Import products and task_id_counter from app module
import app as app_module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_products():
    """Reset products to initial state before each test"""
    # Reset the products list in the app module
    app_module.products.clear()
    app_module.products.extend([
        {
            "id": 1,
            "name": "Laptop Pro 15",
            "category": "Electronics",
            "price": 1299.99,
            "stock": 45,
            "description": "High-performance laptop with 16GB RAM and 512GB SSD",
            "rating": 4.5,
            "created_at": "2024-01-15"
        },
        {
            "id": 2,
            "name": "Wireless Mouse",
            "category": "Accessories",
            "price": 29.99,
            "stock": 150,
            "description": "Ergonomic wireless mouse with USB receiver",
            "rating": 4.2,
            "created_at": "2024-02-20"
        }
    ])
    # Reset the counter
    app_module.product_id_counter = 3
    yield
    # Clean up after test
    app_module.products.clear()
    app_module.products.extend([
        {
            "id": 1,
            "name": "Laptop Pro 15",
            "category": "Electronics",
            "price": 1299.99,
            "stock": 45,
            "description": "High-performance laptop with 16GB RAM and 512GB SSD",
            "rating": 4.5,
            "created_at": "2024-01-15"
        },
        {
            "id": 2,
            "name": "Wireless Mouse",
            "category": "Accessories",
            "price": 29.99,
            "stock": 150,
            "description": "Ergonomic wireless mouse with USB receiver",
            "rating": 4.2,
            "created_at": "2024-02-20"
        }
    ])
    app_module.product_id_counter = 3

# ============ HOME & HEALTH TESTS ============

def test_home(client):
    """Test the home endpoint returns API documentation"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "service" in data
    assert "E-Commerce Product Catalog API" in data["service"]
    assert "endpoints" in data

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "total_products" in data

# ============ GET PRODUCTS TESTS ============

def test_get_all_products(client):
    """Test getting all products"""
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert "total" in data
    assert "products" in data
    assert data["total"] >= 2
    assert isinstance(data["products"], list)

def test_get_products_with_price_filter(client):
    """Test getting products with price range filter"""
    response = client.get('/products?min_price=30&max_price=1500')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] >= 1
    for product in data["products"]:
        assert 30 <= product["price"] <= 1500

def test_get_products_sorted(client):
    """Test getting products sorted by price"""
    response = client.get('/products?sort_by=price&order=asc')
    assert response.status_code == 200
    data = response.get_json()
    prices = [p["price"] for p in data["products"]]
    assert prices == sorted(prices)

def test_get_single_product(client):
    """Test getting a single product by ID"""
    response = client.get('/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Laptop Pro 15"
    assert data["category"] == "Electronics"

def test_get_nonexistent_product(client):
    """Test getting a product that doesn't exist"""
    response = client.get('/products/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "not found" in data["error"].lower()

# ============ CREATE PRODUCT TESTS ============

def test_create_product(client):
    """Test creating a new product"""
    new_product = {
        "name": "Mechanical Keyboard",
        "category": "Accessories",
        "price": 89.99,
        "stock": 30,
        "description": "RGB mechanical keyboard with blue switches",
        "rating": 4.6
    }
    response = client.post('/products', 
                          json=new_product,
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 89.99
    assert "id" in data
    assert "created_at" in data

def test_create_product_missing_required_field(client):
    """Test creating product without required field"""
    incomplete_product = {
        "name": "Test Product",
        "category": "Electronics"
        # Missing price and stock
    }
    response = client.post('/products', 
                          json=incomplete_product,
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field" in data["error"]

def test_create_product_invalid_price(client):
    """Test creating product with invalid price"""
    invalid_product = {
        "name": "Test Product",
        "category": "Electronics",
        "price": -10.00,  # Invalid negative price
        "stock": 10
    }
    response = client.post('/products', 
                          json=invalid_product,
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Price must be greater than 0" in data["error"]

def test_create_product_invalid_stock(client):
    """Test creating product with negative stock"""
    invalid_product = {
        "name": "Test Product",
        "category": "Electronics",
        "price": 50.00,
        "stock": -5  # Invalid negative stock
    }
    response = client.post('/products', 
                          json=invalid_product,
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Stock cannot be negative" in data["error"]

def test_create_product_invalid_category(client):
    """Test creating product with invalid category"""
    invalid_product = {
        "name": "Test Product",
        "category": "InvalidCategory",  # Not in allowed categories
        "price": 50.00,
        "stock": 10
    }
    response = client.post('/products', 
                          json=invalid_product,
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Invalid category" in data["error"]

# ============ UPDATE PRODUCT TESTS ============

def test_update_product(client):
    """Test updating an existing product"""
    update_data = {
        "name": "Laptop Pro 15 Updated",
        "price": 1199.99,
        "stock": 50
    }
    response = client.put('/products/1', 
                         json=update_data,
                         content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Laptop Pro 15 Updated"
    assert data["price"] == 1199.99
    assert data["stock"] == 50

def test_update_nonexistent_product(client):
    """Test updating a product that doesn't exist"""
    update_data = {"name": "Updated Name"}
    response = client.put('/products/9999', 
                         json=update_data,
                         content_type='application/json')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_update_product_invalid_price(client):
    """Test updating product with invalid price"""
    update_data = {"price": -100}
    response = client.put('/products/1', 
                         json=update_data,
                         content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# ============ DELETE PRODUCT TESTS ============

def test_delete_product(client):
    """Test deleting a product"""
    response = client.delete('/products/2')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "deleted successfully" in data["message"].lower()
    
    # Verify it's actually deleted
    get_response = client.get('/products/2')
    assert get_response.status_code == 404

def test_delete_nonexistent_product(client):
    """Test deleting a product that doesn't exist"""
    response = client.delete('/products/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

# ============ SEARCH TESTS ============

def test_search_products_by_name(client):
    """Test searching products by name"""
    response = client.get('/products/search?q=laptop')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_results"] >= 1
    assert "laptop" in data["results"][0]["name"].lower()

def test_search_products_by_category(client):
    """Test searching products by category"""
    response = client.get('/products/search?category=electronics')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_results"] >= 1
    for result in data["results"]:
        assert result["category"].lower() == "electronics"

def test_search_products_no_query(client):
    """Test searching without query parameter"""
    response = client.get('/products/search')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# ============ CATEGORY TESTS ============

def test_get_products_by_category(client):
    """Test getting products filtered by category"""
    response = client.get('/products/category/Electronics')
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == "Electronics"
    assert data["total"] >= 1
    for product in data["products"]:
        assert product["category"] == "Electronics"

def test_get_products_by_empty_category(client):
    """Test getting products from empty category"""
    response = client.get('/products/category/Software')
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 0
    assert data["products"] == []

def test_get_all_categories(client):
    """Test getting all categories"""
    response = client.get('/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert "total" in data
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0

# ============ STATISTICS TESTS ============

def test_get_statistics(client):
    """Test getting catalog statistics"""
    response = client.get('/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_products" in data
    assert "total_inventory_value" in data
    assert "average_price" in data
    assert "average_rating" in data
    assert "total_stock" in data
    assert "categories" in data
    assert data["total_products"] >= 2
    assert data["average_price"] > 0
    assert data["total_stock"] > 0

# ============ INTEGRATION TESTS ============

def test_product_lifecycle(client):
    """Test complete product lifecycle: create, read, update, delete"""
    # Create
    new_product = {
        "name": "Gaming Mouse",
        "category": "Gaming",
        "price": 59.99,
        "stock": 75,
        "description": "High DPI gaming mouse",
        "rating": 4.8
    }
    create_response = client.post('/products', json=new_product)
    assert create_response.status_code == 201
    product_id = create_response.get_json()["id"]
    
    # Read
    read_response = client.get(f'/products/{product_id}')
    assert read_response.status_code == 200
    assert read_response.get_json()["name"] == "Gaming Mouse"
    
    # Update
    update_data = {"price": 54.99, "stock": 80}
    update_response = client.put(f'/products/{product_id}', json=update_data)
    assert update_response.status_code == 200
    assert update_response.get_json()["price"] == 54.99
    
    # Delete
    delete_response = client.delete(f'/products/{product_id}')
    assert delete_response.status_code == 200
    
    # Verify deletion
    verify_response = client.get(f'/products/{product_id}')
    assert verify_response.status_code == 404
