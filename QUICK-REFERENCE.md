# DevSecOps E-Commerce API - Quick Reference Card

## 📋 Project Information

| Item | Value |
|------|-------|
| **Project Name** | devsecops-project |
| **Image Name** | devsecops-project |
| **Container Name** | devsecops-ecommerce-api |
| **Manual Port** | 5000 |
| **Jenkins Port** | 5001 |
| **Jenkins UI** | 8081 |

---

## 🚀 Quick Start Commands

### Local Development
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python app.py

# Run tests
pytest -v

# Security scans
bandit -r .
safety check
```

### Docker Commands
```bash
# Build and run
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up -d --build
```

### Git Commands
```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/devsecops-project.git
git push -u origin main

# Updates
git add .
git commit -m "Your message"
git push origin main
```

---

## 🧪 API Testing Commands

### Basic Endpoints
```bash
# Home
curl http://localhost:5001/

# Health
curl http://localhost:5001/health

# Products
curl http://localhost:5001/products

# Categories
curl http://localhost:5001/categories

# Stats
curl http://localhost:5001/stats
```

### CRUD Operations
```bash
# Create Product
curl -X POST http://localhost:5001/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Product","category":"Electronics","price":99.99,"stock":50}'

# Get Product
curl http://localhost:5001/products/1

# Update Product
curl -X PUT http://localhost:5001/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price":89.99,"stock":60}'

# Delete Product
curl -X DELETE http://localhost:5001/products/1
```

### Search & Filter
```bash
# Search by name
curl "http://localhost:5001/products/search?q=laptop"

# Filter by price
curl "http://localhost:5001/products?min_price=50&max_price=200"

# Sort by price
curl "http://localhost:5001/products?sort_by=price&order=asc"

# Get by category
curl http://localhost:5001/products/category/Electronics
```

---

## 🐳 Docker Management

### Container Operations
```bash
# List containers
docker ps -a

# Start container
docker start devsecops-ecommerce-api

# Stop container
docker stop devsecops-ecommerce-api

# Restart container
docker restart devsecops-ecommerce-api

# Remove container
docker rm devsecops-ecommerce-api

# View logs
docker logs -f devsecops-ecommerce-api
```

### Image Operations
```bash
# List images
docker images

# Build image
docker build -t devsecops-project:latest .

# Remove image
docker rmi devsecops-project:latest

# Clean unused
docker system prune -a
```

### Jenkins Deployment
```bash
# Check Jenkins deployment
docker ps | grep jenkins-devsecops-ecommerce

# View Jenkins deployment logs
docker logs jenkins-devsecops-ecommerce-api -f

# Stop Jenkins deployment
docker-compose -p jenkins-devsecops-ecommerce down
```

---

## 🔧 Jenkins Commands

### Jenkins Container
```bash
# Start Jenkins
docker start jenkins

# Stop Jenkins
docker stop jenkins

# Restart Jenkins
docker restart jenkins

# View logs
docker logs -f jenkins

# Get admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Jenkins Management
```bash
# Access Jenkins
http://localhost:8081

# Create new job
New Item → Pipeline → OK

# Build job
Click "Build Now"

# View console output
Click build number → Console Output
```

---

## 🧪 Testing Commands

### Pytest
```bash
# All tests
pytest

# Verbose
pytest -v

# Very verbose
pytest -vv

# Specific test
pytest test_app.py::test_get_all_products

# With coverage
pytest --cov=app --cov-report=html

# Generate XML report
pytest --junitxml=test-results.xml
```

### Security Scanning
```bash
# Bandit (static code analysis)
bandit -r .
bandit -r . -f json -o bandit-report.json

# Safety (dependency check)
safety check
safety check --json --output safety-report.json

# Trivy (container scan)
trivy image devsecops-project:latest
trivy image --severity HIGH,CRITICAL devsecops-project:latest
```

---

## 🔍 Debugging Commands

### Check Ports
```bash
# List ports in use
lsof -i :5000
lsof -i :5001
lsof -i :8081

# Kill process on port
kill -9 <PID>
```

### Check Processes
```bash
# List Python processes
ps aux | grep python

# List Docker processes
ps aux | grep docker

# System resources
top
htop
```

### Network Testing
```bash
# Check connectivity
ping localhost
curl -I http://localhost:5001

# Check DNS
nslookup localhost

# Network interfaces
ifconfig
ip addr show
```

---

## 📊 Monitoring Commands

### Container Stats
```bash
# All containers
docker stats

# Specific container
docker stats devsecops-ecommerce-api

# One-time snapshot
docker stats --no-stream
```

### Disk Usage
```bash
# Docker disk usage
docker system df

# Detailed view
docker system df -v

# Container sizes
docker ps --size
```

### Logs Analysis
```bash
# Last 50 lines
docker logs --tail 50 devsecops-ecommerce-api

# Follow logs
docker logs -f devsecops-ecommerce-api

# With timestamps
docker logs -t devsecops-ecommerce-api

# Since timestamp
docker logs --since 2024-01-01T00:00:00 devsecops-ecommerce-api
```

---

## 🆘 Troubleshooting

### Port Conflicts
```bash
# Find process
lsof -i :5001

# Kill and restart
kill -9 <PID>
docker-compose up -d
```

### Container Won't Start
```bash
# Check logs
docker logs devsecops-ecommerce-api

# Inspect container
docker inspect devsecops-ecommerce-api

# Remove and recreate
docker rm devsecops-ecommerce-api
docker-compose up -d
```

### Tests Failing
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear cache
rm -rf __pycache__ .pytest_cache
pytest -v
```

### Docker Issues
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Clean everything
docker system prune -a --volumes

# Reset Docker Desktop
# Settings → Troubleshoot → Reset to factory defaults
```

---

## 📁 File Locations

### Project Files
```
devsecops-project/
├── app.py                 # Flask application
├── test_app.py            # Test cases
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker image
├── docker-compose.yml     # Compose config
├── Jenkinsfile           # Pipeline
├── .gitignore            # Git ignore
└── README.md             # Documentation
```

### Generated Files (gitignored)
```
venv/                     # Virtual environment
__pycache__/             # Python cache
.pytest_cache/           # Pytest cache
test-results.xml         # Test report
bandit-report.json       # Security scan
safety-report.json       # Dependency scan
trivy-report.json        # Container scan
docker-compose.jenkins.yml  # Jenkins compose
```

---

## 🌐 Useful URLs

| Service | URL |
|---------|-----|
| **Manual App** | http://localhost:5000 |
| **Jenkins App** | http://localhost:5001 |
| **Jenkins UI** | http://localhost:8081 |
| **API Docs** | http://localhost:5001/ |
| **Health Check** | http://localhost:5001/health |
| **Products** | http://localhost:5001/products |
| **Stats** | http://localhost:5001/stats |

---

## 🔑 Environment Variables

### For Development
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### For Production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-secret-key
```

### Docker Compose
```yaml
environment:
  - FLASK_ENV=production
  - SECRET_KEY=${SECRET_KEY}
```

---

## 📝 Common Workflows

### Daily Development
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Pull latest changes
git pull origin main

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest -v

# 5. Run app
python app.py
```

### Before Commit
```bash
# 1. Run tests
pytest -v

# 2. Run security scans
bandit -r .
safety check

# 3. Format code (optional)
black app.py test_app.py

# 4. Add and commit
git add .
git commit -m "Description"
git push origin main
```

### Deploy Update
```bash
# 1. Stop current deployment
docker-compose down

# 2. Pull changes
git pull origin main

# 3. Rebuild and restart
docker-compose up -d --build

# 4. Verify
curl http://localhost:5000/health
```

### Jenkins Build
```bash
# 1. Push to GitHub
git push origin main

# 2. Trigger Jenkins build
# - Auto (with webhook)
# - Manual (Build Now)

# 3. Monitor build
# - Console Output

# 4. Verify deployment
curl http://localhost:5001/health
```

---

## 🎯 Performance Tips

### Docker Optimization
```bash
# Use BuildKit
export DOCKER_BUILDKIT=1
docker build -t devsecops-project:latest .

# Multi-stage builds
# See Dockerfile for example

# Clean cache regularly
docker system prune -a
```

### Application Optimization
```python
# Add caching
from flask_caching import Cache
cache = Cache(app)

# Add compression
from flask_compress import Compress
compress = Compress(app)

# Add rate limiting
from flask_limiter import Limiter
limiter = Limiter(app)
```

---

## 📚 Quick Reference Links

### Documentation
- Flask: https://flask.palletsprojects.com/
- Docker: https://docs.docker.com/
- Jenkins: https://www.jenkins.io/doc/
- Pytest: https://docs.pytest.org/

### Tools
- Postman: https://www.postman.com/
- Docker Desktop: https://www.docker.com/products/docker-desktop
- VS Code: https://code.visualstudio.com/

### GitHub
- Project: https://github.com/YOUR_USERNAME/devsecops-project
- Issues: https://github.com/YOUR_USERNAME/devsecops-project/issues

---

## 💡 Pro Tips

1. **Always test locally before pushing**
   ```bash
   pytest -v && bandit -r . && safety check
   ```

2. **Use aliases for common commands**
   ```bash
   alias dcu='docker-compose up -d'
   alias dcd='docker-compose down'
   alias dcl='docker-compose logs -f'
   ```

3. **Keep Jenkins artifacts**
   - Download reports after each build
   - Track security trends over time

4. **Monitor resource usage**
   ```bash
   docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
   ```

5. **Backup important data**
   ```bash
   # Jenkins home
   docker exec jenkins tar czf /tmp/jenkins-backup.tar.gz /var/jenkins_home
   docker cp jenkins:/tmp/jenkins-backup.tar.gz ./
   ```

---

**Quick Reference Card Version:** 1.0  
**Last Updated:** November 2025  
**Print this for quick access!** 📄
