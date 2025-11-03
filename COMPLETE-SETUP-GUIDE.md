# E-Commerce API DevSecOps Project - Complete Setup Guide

## 🎯 Project Overview

**Project Name:** devsecops-project  
**Application:** E-Commerce Product Catalog REST API  
**Image Name:** devsecops-project  
**Container Name:** devsecops-ecommerce-api  

### What Changed from Task Manager Project?

| Component | Task Manager | E-Commerce API |
|-----------|-------------|----------------|
| **Application Type** | Task Management API | Product Catalog API |
| **Main Entities** | Tasks | Products |
| **Image Name** | python-devsecops-jenkins_app | devsecops-project |
| **Container Name** | lab2-web-1 | devsecops-ecommerce-api |
| **Project Name** | jenkins-devsecops | jenkins-devsecops-ecommerce |
| **Features** | 5 CRUD endpoints | 13+ endpoints with advanced features |
| **Test Cases** | 10 tests | 20+ comprehensive tests |

---

## 📁 Complete File Structure

```
devsecops-project/
├── app.py                      # E-Commerce API (Flask application)
├── test_app.py                 # 20+ comprehensive test cases
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── Jenkinsfile                 # Jenkins CI/CD pipeline
├── .gitignore                  # Git ignore patterns
└── README.md                   # Project documentation
```

---

## 🚀 Step-by-Step Setup Guide

### Step 1: Create Project Directory and Files

```bash
# Create project directory
mkdir devsecops-project
cd devsecops-project

# Initialize git
git init
```

### Step 2: Create Application Files

#### 2.1 Create `app.py` (E-Commerce Product Catalog API)

**Key Features:**
- ✅ Product CRUD operations
- ✅ Advanced search and filtering
- ✅ Category management
- ✅ Price range filtering
- ✅ Product ratings
- ✅ Real-time statistics
- ✅ 13+ REST endpoints

**Main Endpoints:**
```python
GET  /                              # API documentation
GET  /health                        # Health check
GET  /products                      # List all products (with filters)
POST /products                      # Create product
GET  /products/<id>                 # Get specific product
PUT  /products/<id>                 # Update product
DELETE /products/<id>               # Delete product
GET  /products/search               # Search products
GET  /products/category/<category>  # Get by category
GET  /categories                    # List categories
GET  /stats                         # Catalog statistics
```

Create the file with the full Flask application code (provided in app.py).

#### 2.2 Create `test_app.py` (20+ Test Cases)

**Test Coverage:**
- ✅ Home & Health endpoints
- ✅ GET operations (all products, single product, filtering)
- ✅ POST operations (create, validation)
- ✅ PUT operations (update, validation)
- ✅ DELETE operations
- ✅ Search & filter functionality
- ✅ Category operations
- ✅ Statistics endpoint
- ✅ Integration tests (complete lifecycle)

Create the file with comprehensive test suite (provided in test_app.py).

#### 2.3 Create `requirements.txt`

```txt
Flask==2.3.0
Werkzeug==2.3.0
pytest==7.3.1
bandit==1.7.5
safety==2.3.5
```

#### 2.4 Create `Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
CMD ["python3", "app.py"]
```

#### 2.5 Create `docker-compose.yml`

```yaml
version: '3.8'
services:
  web:
    build: .
    image: devsecops-project
    container_name: devsecops-ecommerce-api
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

**Key Changes:**
- Image name: `devsecops-project`
- Container name: `devsecops-ecommerce-api`

#### 2.6 Create `Jenkinsfile`

**Pipeline Configuration:**
- Project name: `jenkins-devsecops-ecommerce`
- Image name: `devsecops-project`
- Deployment port: `5001` (to avoid conflicts)
- Enhanced verification with multiple endpoint tests

Create the file with the complete pipeline definition (provided in Jenkinsfile).

#### 2.7 Create `.gitignore`

```
__pycache__/
*.py[cod]
venv/
.pytest_cache/
test-results.xml
bandit-report.json
safety-report.json
trivy-report.json
.vscode/
.idea/
docker-compose.jenkins.yml
.DS_Store
```

#### 2.8 Create `README.md`

Comprehensive documentation with:
- API documentation
- Quick start guide
- Testing instructions
- Deployment steps
- API examples with curl commands

---

## 🧪 Local Testing (Before Pushing to GitHub)

### Test 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Test 2: Run Application Locally

```bash
# Run the Flask app
python app.py

# Should see:
# * Running on http://0.0.0.0:5000
```

### Test 3: Test API Endpoints

Open a new terminal:

```bash
# Test home endpoint
curl http://localhost:5000/

# Test health check
curl http://localhost:5000/health

# Test products endpoint
curl http://localhost:5000/products

# Test categories
curl http://localhost:5000/categories

# Test statistics
curl http://localhost:5000/stats
```

### Test 4: Run Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest -v

# Expected output: All 20+ tests should pass
```

### Test 5: Run Security Scans

```bash
# Bandit security scan
bandit -r .

# Safety dependency check
safety check

# Expected: Some warnings are normal, but no critical issues
```

### Test 6: Docker Build

```bash
# Build Docker image
docker build -t devsecops-project:latest .

# Run container
docker run -d -p 5000:5000 --name test-api devsecops-project:latest

# Test the containerized API
curl http://localhost:5000/health

# Stop and remove
docker stop test-api
docker rm test-api
```

### Test 7: Docker Compose

```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test API
curl http://localhost:5000/products

# Stop
docker-compose down
```

---

## 📤 Push to GitHub

### Step 1: Create Repository on GitHub

1. Go to https://github.com
2. Click "New repository"
3. Repository name: `devsecops-project`
4. Description: "E-Commerce Product Catalog API with DevSecOps Pipeline"
5. Public or Private (your choice)
6. Do NOT initialize with README (we already have one)
7. Click "Create repository"

### Step 2: Add All Files to Git

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: E-Commerce API with DevSecOps pipeline"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/devsecops-project.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

Go to your repository and verify all files are present:
- ✅ app.py
- ✅ test_app.py
- ✅ requirements.txt
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ Jenkinsfile
- ✅ .gitignore
- ✅ README.md

---

## 🔧 Jenkins Setup

### Step 1: Ensure Jenkins is Running

```bash
# Check if Jenkins container exists
docker ps -a | grep jenkins

# If not running, start it
docker start jenkins

# If doesn't exist, create it
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk11

# Get admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 2: Access Jenkins

1. Open browser: `http://localhost:8081`
2. Enter admin password
3. Install suggested plugins
4. Create admin user
5. Configure Jenkins URL: `http://localhost:8081`

### Step 3: Install Required Plugins

Go to **Manage Jenkins** → **Manage Plugins** → **Available**

Install:
- ✅ Docker Pipeline
- ✅ Docker plugin
- ✅ Git plugin
- ✅ Pipeline plugin
- ✅ JUnit plugin

Restart Jenkins after installation.

### Step 4: Create New Pipeline Job

1. Click **New Item**
2. Enter name: `ecommerce-api-pipeline`
3. Select **Pipeline**
4. Click **OK**

### Step 5: Configure Pipeline

**General:**
- Description: "E-Commerce API DevSecOps Pipeline"

**Build Triggers (Optional):**
- ☑️ GitHub hook trigger for GITScm polling
- ☑️ Poll SCM: `H/5 * * * *`

**Pipeline:**
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/YOUR_USERNAME/devsecops-project.git`
- Credentials: Add if private repository
- Branch Specifier: `*/main`
- Script Path: `Jenkinsfile`

Click **Save**.

### Step 6: Run First Build

1. Click **Build Now**
2. Watch **Console Output**
3. Monitor each stage:
   - ✅ Checkout
   - ✅ Install Dependencies
   - ✅ Run Tests (20+ tests)
   - ✅ Static Code Analysis (Bandit)
   - ✅ Dependency Vulnerabilities (Safety)
   - ✅ Cleanup Previous Deployment
   - ✅ Build Docker Image
   - ✅ Container Vulnerability Scan (Trivy)
   - ✅ Deploy Application
   - ✅ Verify Deployment

### Step 7: Verify Deployment

After successful build:

```bash
# Check running containers
docker ps | grep jenkins-devsecops-ecommerce

# Test deployed API
curl http://localhost:5001/
curl http://localhost:5001/health
curl http://localhost:5001/products
curl http://localhost:5001/categories
curl http://localhost:5001/stats
```

---

## 🎯 Testing the Deployed API

### Basic Endpoints

```bash
# 1. API Documentation
curl http://localhost:5001/

# 2. Health Check
curl http://localhost:5001/health

# 3. Get All Products
curl http://localhost:5001/products

# 4. Get Single Product
curl http://localhost:5001/products/1

# 5. Get Categories
curl http://localhost:5001/categories

# 6. Get Statistics
curl http://localhost:5001/stats
```

### Advanced Operations

```bash
# 7. Create New Product
curl -X POST http://localhost:5001/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Monitor",
    "category": "Electronics",
    "price": 399.99,
    "stock": 25,
    "description": "27-inch 144Hz gaming monitor",
    "rating": 4.8
  }'

# 8. Update Product
curl -X PUT http://localhost:5001/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1249.99,
    "stock": 60
  }'

# 9. Search Products
curl "http://localhost:5001/products/search?q=laptop"

# 10. Filter by Price Range
curl "http://localhost:5001/products?min_price=30&max_price=100"

# 11. Get Products by Category
curl http://localhost:5001/products/category/Electronics

# 12. Sort Products by Price
curl "http://localhost:5001/products?sort_by=price&order=asc"

# 13. Delete Product
curl -X DELETE http://localhost:5001/products/2
```

### Test with JSON Pretty Print

```bash
# Install jq for pretty JSON
# Ubuntu/Debian: sudo apt install jq
# macOS: brew install jq

# Pretty print products
curl -s http://localhost:5001/products | jq

# Pretty print statistics
curl -s http://localhost:5001/stats | jq
```

---

## 📊 Monitoring and Logs

### View Container Logs

```bash
# Jenkins deployment logs
docker logs jenkins-devsecops-ecommerce-api -f

# Manual deployment logs (if running)
docker logs devsecops-ecommerce-api -f
```

### Check Container Status

```bash
# List all containers
docker ps -a

# Check specific container
docker ps --filter "name=jenkins-devsecops-ecommerce"

# View container details
docker inspect jenkins-devsecops-ecommerce-api
```

### View Jenkins Artifacts

1. Go to Jenkins build page
2. Click on build number
3. Click **Artifacts**
4. Download:
   - `test-results.xml` - Test results
   - `bandit-report.json` - Security scan
   - `safety-report.json` - Dependency vulnerabilities
   - `trivy-report.json` - Container vulnerabilities

---

## 🔄 Updating the Application

### Method 1: Push Changes to GitHub

```bash
# Make changes to app.py or other files
nano app.py

# Add and commit
git add .
git commit -m "Update: Added new feature"

# Push to GitHub
git push origin main

# Jenkins will automatically trigger build (if webhook configured)
# Or manually trigger: Go to Jenkins → Build Now
```

### Method 2: Manual Rebuild

```bash
# Stop current deployment
docker-compose down

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

---

## 🐛 Troubleshooting

### Issue 1: Port 5001 Already in Use

```bash
# Find process using port
lsof -i :5001

# Kill process
kill -9 <PID>

# Or change APP_PORT in Jenkinsfile
# Change line: APP_PORT = '5002'
```

### Issue 2: Jenkins Can't Access Docker

```bash
# Restart Jenkins container
docker restart jenkins

# Check Docker socket mount
docker inspect jenkins | grep docker.sock

# Re-create with proper mount if needed
docker rm jenkins
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --user root \
  jenkins/jenkins:lts-jdk11
```

### Issue 3: Tests Failing

```bash
# Check if virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run specific test
pytest test_app.py::test_get_all_products -v

# Run with more verbosity
pytest -vv
```

### Issue 4: Docker Build Fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t devsecops-project:latest .

# Check Dockerfile syntax
docker build -t devsecops-project:latest . --progress=plain
```

### Issue 5: API Not Responding

```bash
# Check if container is running
docker ps | grep devsecops

# Check container logs
docker logs jenkins-devsecops-ecommerce-api

# Check container health
docker inspect jenkins-devsecops-ecommerce-api | grep Health

# Restart container
docker restart jenkins-devsecops-ecommerce-api
```

---

## 🔒 Security Best Practices

### 1. Regular Updates

```bash
# Update Python packages
pip list --outdated
pip install --upgrade <package>

# Update Docker base image
# Change in Dockerfile: FROM python:3.9-slim → python:3.10-slim
```

### 2. Review Security Reports

After each build, review:
- **Bandit Report**: Check for code security issues
- **Safety Report**: Check for vulnerable dependencies
- **Trivy Report**: Check for container vulnerabilities

### 3. Environment Variables

For production, use environment variables:

```bash
# In docker-compose.yml
environment:
  - FLASK_SECRET_KEY=${SECRET_KEY}
  - DATABASE_URL=${DATABASE_URL}
  - API_KEY=${API_KEY}
```

### 4. HTTPS Configuration

For production, use reverse proxy (nginx):

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📈 Performance Optimization

### 1. Add Redis Caching

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/products')
@cache.cached(timeout=60)
def get_products():
    # Cached for 60 seconds
    pass
```

### 2. Add Database

Replace in-memory storage:

```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
db = SQLAlchemy(app)
```

### 3. Add Gunicorn

```dockerfile
# In Dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🎓 Learning Outcomes

By completing this project, you've learned:

✅ **DevSecOps Practices**
- CI/CD pipeline implementation
- Security scanning integration
- Automated testing

✅ **Flask Development**
- REST API design
- CRUD operations
- Request handling
- Error handling

✅ **Docker & Containerization**
- Dockerfile creation
- Docker Compose
- Container management
- Image optimization

✅ **Testing**
- Unit testing with Pytest
- Integration testing
- Test coverage
- Continuous testing

✅ **Security**
- Static code analysis
- Dependency scanning
- Container scanning
- Security best practices

✅ **Jenkins**
- Pipeline as code
- Multi-stage builds
- Artifact management
- Deployment automation

---

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- [Pytest Documentation](https://docs.pytest.org/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [Insomnia](https://insomnia.rest/) - API testing
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Security Tools
- [Bandit](https://bandit.readthedocs.io/)
- [Safety](https://pyup.io/safety/)
- [Trivy](https://aquasecurity.github.io/trivy/)

---

## 🎉 Conclusion

You now have a complete E-Commerce Product Catalog API with:

✅ Full CRUD functionality  
✅ 20+ test cases  
✅ Security scanning  
✅ Automated CI/CD  
✅ Docker deployment  
✅ Comprehensive documentation  

### Next Steps

1. **Extend the API**: Add more features
   - User authentication
   - Order management
   - Payment processing
   - Image upload

2. **Add Database**: Implement persistent storage
   - PostgreSQL
   - MongoDB
   - Redis caching

3. **Deploy to Cloud**: Move to production
   - AWS ECS/EKS
   - Google Cloud Run
   - Azure Container Instances
   - Heroku

4. **Monitoring**: Add observability
   - Prometheus
   - Grafana
   - ELK Stack
   - Application Performance Monitoring

5. **Scale**: Implement microservices
   - Break into smaller services
   - Add API Gateway
   - Implement service mesh
   - Add load balancing

---

**Project:** devsecops-project  
**Version:** 1.0.0  
**Status:** Production Ready ✅  
**Last Updated:** November 2025

Happy Coding! 🚀
