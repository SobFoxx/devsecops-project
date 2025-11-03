# E-Commerce Product Catalog API - DevSecOps Project

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

A production-ready E-Commerce Product Catalog REST API with complete DevSecOps CI/CD pipeline using Jenkins, Docker, and comprehensive security scanning.

## 🌟 Features

### Application Features
- 📦 Complete Product Management (CRUD operations)
- 🔍 Advanced Product Search and Filtering
- 📊 Category Management
- 📈 Real-time Statistics and Analytics
- 💰 Price Range Filtering
- ⭐ Product Ratings
- 🏷️ Multi-category Support
- 🔄 RESTful API Design

### DevSecOps Features
- 🐍 Automated Testing with Pytest (20+ test cases)
- 🔒 Static Code Analysis (Bandit)
- 🛡️ Dependency Vulnerability Scanning (Safety)
- 🐳 Container Security Scanning (Trivy)
- 🚀 Automated CI/CD with Jenkins
- 📊 Test Reports and Artifacts
- 🔄 Continuous Integration
- 📦 Dockerized Deployment

## 📋 Table of Contents

- [API Documentation](#api-documentation)
- [Quick Start](#quick-start)
- [Testing](#testing)
- [DevSecOps Pipeline](#devsecops-pipeline)
- [Deployment](#deployment)
- [API Examples](#api-examples)
- [Security](#security)
- [Contributing](#contributing)

## 🚀 API Documentation

### Base URL
```
http://localhost:5000 (Manual Deployment)
http://localhost:5001 (Jenkins Deployment)
```

### Endpoints

#### General Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation and available endpoints |
| GET | `/health` | Health check endpoint |
| GET | `/stats` | Get catalog statistics |
| GET | `/categories` | Get all available categories |

#### Product Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products (with optional filters) |
| POST | `/products` | Create a new product |
| GET | `/products/<id>` | Get specific product by ID |
| PUT | `/products/<id>` | Update product by ID |
| DELETE | `/products/<id>` | Delete product by ID |
| GET | `/products/search` | Search products by name or category |
| GET | `/products/category/<category>` | Get products by category |

### Query Parameters

#### `/products` Endpoint
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `sort_by` (string): Sort field (id, name, price, rating, stock)
- `order` (string): Sort order (asc, desc)

Example:
```bash
GET /products?min_price=20&max_price=100&sort_by=price&order=asc
```

#### `/products/search` Endpoint
- `q` (string): Search query for product name
- `category` (string): Filter by category

Example:
```bash
GET /products/search?q=laptop&category=electronics
```

### Response Format

#### Success Response
```json
{
  "id": 1,
  "name": "Product Name",
  "category": "Electronics",
  "price": 99.99,
  "stock": 50,
  "description": "Product description",
  "rating": 4.5,
  "created_at": "2024-01-15"
}
```

#### Error Response
```json
{
  "error": "Error message description"
}
```

### Available Categories
- Electronics
- Accessories
- Software
- Books
- Gaming

## 🏁 Quick Start

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Git
- Jenkins (for CI/CD)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/devsecops-project.git
cd devsecops-project
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the API**
```
http://localhost:5000
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Check container status**
```bash
docker-compose ps
```

3. **View logs**
```bash
docker-compose logs -f
```

4. **Stop the application**
```bash
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t devsecops-project:latest .

# Run container
docker run -d -p 5000:5000 --name ecommerce-api devsecops-project:latest

# Check logs
docker logs -f ecommerce-api
```

## 🧪 Testing

### Run All Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Categories

The test suite includes 20+ comprehensive tests:

- ✅ Home & Health Endpoint Tests
- ✅ GET Product Tests (all products, single product, filtering)
- ✅ POST Product Tests (create, validation)
- ✅ PUT Product Tests (update, validation)
- ✅ DELETE Product Tests
- ✅ Search & Filter Tests
- ✅ Category Tests
- ✅ Statistics Tests
- ✅ Integration Tests (complete lifecycle)

### Security Scanning

#### Static Code Analysis (Bandit)
```bash
source venv/bin/activate
bandit -r . -f json -o bandit-report.json
```

#### Dependency Vulnerability Check (Safety)
```bash
source venv/bin/activate
safety check
```

#### Container Vulnerability Scan (Trivy)
```bash
trivy image devsecops-project:latest
```

## 🔄 DevSecOps Pipeline

### Pipeline Stages

1. **Checkout** - Clone repository from GitHub
2. **Install Dependencies** - Set up Python virtual environment
3. **Run Tests** - Execute 20+ Pytest test cases
4. **Static Code Analysis** - Bandit security scan
5. **Dependency Vulnerabilities** - Safety check
6. **Cleanup** - Remove previous deployment
7. **Build Docker Image** - Create container image
8. **Container Scan** - Trivy vulnerability scan
9. **Deploy** - Deploy to port 5001
10. **Verify** - Health checks and endpoint testing

### Jenkins Setup

1. **Install Jenkins**
```bash
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk11
```

2. **Get Initial Password**
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

3. **Install Required Plugins**
- Docker Pipeline
- Git Plugin
- Pipeline Plugin
- JUnit Plugin

4. **Create Pipeline Job**
- New Item → Pipeline
- Name: `ecommerce-devsecops-pipeline`
- Pipeline script from SCM
- Repository URL: Your GitHub repo
- Script Path: `Jenkinsfile`

### View Pipeline Reports

After pipeline execution, check:
- **Test Results**: JUnit test report
- **Security Reports**: Bandit, Safety, Trivy JSON reports
- **Build Artifacts**: All reports archived

## 📦 API Examples

### 1. Get API Documentation
```bash
curl http://localhost:5000/
```

### 2. Health Check
```bash
curl http://localhost:5000/health
```

### 3. Get All Products
```bash
curl http://localhost:5000/products
```

### 4. Get Products with Price Filter
```bash
curl "http://localhost:5000/products?min_price=30&max_price=100"
```

### 5. Get Products Sorted by Price
```bash
curl "http://localhost:5000/products?sort_by=price&order=asc"
```

### 6. Get Specific Product
```bash
curl http://localhost:5000/products/1
```

### 7. Create New Product
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "category": "Electronics",
    "price": 79.99,
    "stock": 100,
    "description": "Premium wireless headphones with noise cancellation",
    "rating": 4.7
  }'
```

### 8. Update Product
```bash
curl -X PUT http://localhost:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99,
    "stock": 55
  }'
```

### 9. Delete Product
```bash
curl -X DELETE http://localhost:5000/products/2
```

### 10. Search Products
```bash
# Search by name
curl "http://localhost:5000/products/search?q=laptop"

# Search by category
curl "http://localhost:5000/products/search?category=electronics"
```

### 11. Get Products by Category
```bash
curl http://localhost:5000/products/category/Electronics
```

### 12. Get All Categories
```bash
curl http://localhost:5000/categories
```

### 13. Get Catalog Statistics
```bash
curl http://localhost:5000/stats
```

### Response Examples

#### Get All Products Response
```json
{
  "total": 3,
  "products": [
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
  ]
}
```

#### Statistics Response
```json
{
  "total_products": 3,
  "total_inventory_value": 65849.25,
  "average_price": 459.99,
  "average_rating": 4.47,
  "total_stock": 275,
  "categories": {
    "Electronics": {
      "count": 1,
      "total_stock": 45
    },
    "Accessories": {
      "count": 2,
      "total_stock": 230
    }
  }
}
```

## 🔒 Security

### Security Features

1. **Input Validation**
   - Required field validation
   - Data type validation
   - Price and stock validation
   - Category validation

2. **Static Code Analysis**
   - Bandit scans for common security issues
   - SQL injection prevention
   - XSS prevention
   - Hardcoded credentials detection

3. **Dependency Scanning**
   - Safety checks for vulnerable packages
   - Regular dependency updates

4. **Container Security**
   - Trivy scans for vulnerabilities
   - Minimal base image (python:3.9-slim)
   - Regular image updates

### Best Practices Implemented

- ✅ Input sanitization
- ✅ Error handling
- ✅ No hardcoded secrets
- ✅ HTTPS ready (configure reverse proxy)
- ✅ Rate limiting ready (add middleware)
- ✅ CORS configurable
- ✅ Environment-based configuration

## 📊 Project Structure

```
devsecops-project/
├── app.py                      # Main Flask application
├── test_app.py                 # Pytest test suite
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── Jenkinsfile                 # Jenkins pipeline definition
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🛠️ Technologies Used

- **Backend**: Python 3.9, Flask 2.3.0
- **Testing**: Pytest 7.3.1
- **Security**: Bandit 1.7.5, Safety 2.3.5, Trivy
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Version Control**: Git, GitHub

## 📈 Performance

- **Lightweight**: Minimal dependencies
- **Fast Response**: In-memory data store
- **Scalable**: Stateless design
- **Container-ready**: Optimized Docker image

## 🚀 Production Considerations

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-secret-key
```

### Add Database
Replace in-memory storage with:
- PostgreSQL
- MongoDB
- Redis (caching)

### Add Authentication
- JWT tokens
- OAuth 2.0
- API keys

### Add Rate Limiting
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

### Add CORS
```python
from flask_cors import CORS
CORS(app)
```

### Add Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
export PORT=5001
```

### Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t devsecops-project:latest .
```

### Tests Fail
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run specific test
pytest test_app.py::test_name -v
```

### Jenkins Pipeline Fails
```bash
# Check Jenkins logs
docker logs jenkins -f

# Verify Docker socket access
docker exec jenkins docker ps

# Restart Jenkins
docker restart jenkins
```

## 📝 License

MIT License - feel free to use this project for learning and development.

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Flask team for the excellent framework
- Jenkins community for CI/CD tools
- Docker for containerization
- Security tool maintainers (Bandit, Safety, Trivy)

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** Production Ready ✅
