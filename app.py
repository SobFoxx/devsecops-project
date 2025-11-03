from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

# In-memory product catalog
products = [
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
    },
    {
        "id": 3,
        "name": "USB-C Hub",
        "category": "Accessories",
        "price": 49.99,
        "stock": 80,
        "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
        "rating": 4.7,
        "created_at": "2024-03-10"
    }
]

categories = ["Electronics", "Accessories", "Software", "Books", "Gaming"]
product_id_counter = 4

@app.route('/')
def home():
    return jsonify({
        "service": "E-Commerce Product Catalog API",
        "version": "1.0.0",
        "description": "RESTful API for managing product catalog",
        "endpoints": {
            "/products": "GET - List all products, POST - Add new product",
            "/products/<id>": "GET - Get product details, PUT - Update product, DELETE - Remove product",
            "/products/search": "GET - Search products by name or category",
            "/products/category/<category>": "GET - Get products by category",
            "/categories": "GET - List all categories",
            "/stats": "GET - Get catalog statistics",
            "/health": "GET - Health check endpoint"
        }
    }), 200

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_products": len(products)
    }), 200

@app.route('/products', methods=['GET'])
def get_products():
    # Optional query parameters for filtering and sorting
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    
    filtered_products = products.copy()
    
    # Filter by price range
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]
    
    # Sort products
    reverse = (order == 'desc')
    try:
        filtered_products.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    except:
        pass
    
    return jsonify({
        "total": len(filtered_products),
        "products": filtered_products
    }), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(product), 200

@app.route('/products', methods=['POST'])
def create_product():
    global product_id_counter
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'category', 'price', 'stock']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate price and stock
    if data['price'] <= 0:
        return jsonify({"error": "Price must be greater than 0"}), 400
    if data['stock'] < 0:
        return jsonify({"error": "Stock cannot be negative"}), 400
    
    # Validate category
    if data['category'] not in categories:
        return jsonify({"error": f"Invalid category. Choose from: {', '.join(categories)}"}), 400
    
    product = {
        "id": product_id_counter,
        "name": data['name'],
        "category": data['category'],
        "price": float(data['price']),
        "stock": int(data['stock']),
        "description": data.get('description', ''),
        "rating": data.get('rating', 0.0),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    products.append(product)
    product_id_counter += 1
    
    return jsonify(product), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        product['name'] = data['name']
    if 'category' in data:
        if data['category'] not in categories:
            return jsonify({"error": f"Invalid category. Choose from: {', '.join(categories)}"}), 400
        product['category'] = data['category']
    if 'price' in data:
        if data['price'] <= 0:
            return jsonify({"error": "Price must be greater than 0"}), 400
        product['price'] = float(data['price'])
    if 'stock' in data:
        if data['stock'] < 0:
            return jsonify({"error": "Stock cannot be negative"}), 400
        product['stock'] = int(data['stock'])
    if 'description' in data:
        product['description'] = data['description']
    if 'rating' in data:
        product['rating'] = float(data['rating'])
    
    return jsonify(product), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    products = [p for p in products if p['id'] != product_id]
    
    return jsonify({
        "message": "Product deleted successfully",
        "product_id": product_id
    }), 200

@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    
    if not query and not category:
        return jsonify({"error": "Please provide 'q' (query) or 'category' parameter"}), 400
    
    results = []
    for product in products:
        matches = False
        if query and query in product['name'].lower():
            matches = True
        if category and category in product['category'].lower():
            matches = True
        if matches:
            results.append(product)
    
    return jsonify({
        "query": query,
        "category": category,
        "total_results": len(results),
        "results": results
    }), 200

@app.route('/products/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    category_products = [p for p in products if p['category'].lower() == category.lower()]
    
    if not category_products:
        return jsonify({
            "category": category,
            "total": 0,
            "products": []
        }), 200
    
    return jsonify({
        "category": category,
        "total": len(category_products),
        "products": category_products
    }), 200

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({
        "total": len(categories),
        "categories": categories
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    total_value = sum(p['price'] * p['stock'] for p in products)
    avg_price = sum(p['price'] for p in products) / len(products) if products else 0
    avg_rating = sum(p['rating'] for p in products) / len(products) if products else 0
    
    category_stats = {}
    for category in categories:
        cat_products = [p for p in products if p['category'] == category]
        category_stats[category] = {
            "count": len(cat_products),
            "total_stock": sum(p['stock'] for p in cat_products)
        }
    
    return jsonify({
        "total_products": len(products),
        "total_inventory_value": round(total_value, 2),
        "average_price": round(avg_price, 2),
        "average_rating": round(avg_rating, 2),
        "total_stock": sum(p['stock'] for p in products),
        "categories": category_stats
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
