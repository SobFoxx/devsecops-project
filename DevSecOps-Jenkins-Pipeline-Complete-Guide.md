# Complete DevSecOps Jenkins Pipeline Implementation Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides a complete implementation of a DevSecOps pipeline using Jenkins, Docker, and various security scanning tools. The pipeline includes:

- ✅ Python application with Flask
- ✅ Automated testing with Pytest
- ✅ Static code analysis with Bandit
- ✅ Dependency vulnerability scanning with Safety
- ✅ Container vulnerability scanning with Trivy
- ✅ Dockerized deployment
- ✅ Automated CI/CD with Jenkins

**Architecture:**
```
GitHub Repository → Jenkins Pipeline → Docker Build → Security Scans → Deployment
```

---

## Prerequisites

### System Requirements
- Docker installed and running
- Docker Compose installed
- Git installed
- GitHub account
- At least 4GB RAM
- 10GB free disk space

### Ports Used
- `5000` - Original Python application (lab2-web-1)
- `5001` - Jenkins-deployed application
- `8081` - Jenkins web interface
- `50000` - Jenkins agent communication

---

## Project Structure

```
jenkins-devsecops-project/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── test_app.py                # Pytest test cases
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── Jenkinsfile               # Jenkins pipeline definition
└── README.md                 # Project documentation
```

---

## Step-by-Step Implementation

### Step 1: Create Project Directory

```bash
# Create project directory
mkdir jenkins-devsecops-project
cd jenkins-devsecops-project

# Initialize git repository
git init
```

---

### Step 2: Create Python Flask Application

**File: `app.py`**

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the DevSecOps Task Manager API",
        "endpoints": {
            "/tasks": "GET - List all tasks, POST - Create a task",
            "/tasks/<id>": "GET - Get task, PUT - Update task, DELETE - Delete task"
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = {
        "id": task_id_counter,
        "title": data['title'],
        "description": data.get('description', ''),
        "completed": False
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

### Step 3: Create Requirements File

**File: `requirements.txt`**

```txt
Flask==2.3.0
Werkzeug==2.3.0
pytest==7.3.1
bandit==1.7.5
safety==2.3.5
```

---

### Step 4: Create Test File

**File: `test_app.py`**

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "Welcome" in data["message"]

def test_get_tasks_empty(client):
    """Test getting tasks when list is empty"""
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

def test_create_task(client):
    """Test creating a new task"""
    response = client.post('/tasks', 
                          json={'title': 'Test Task', 'description': 'Test Description'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert data['completed'] == False

def test_create_task_without_title(client):
    """Test creating a task without title (should fail)"""
    response = client.post('/tasks', json={'description': 'Test Description'})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_get_task(client):
    """Test getting a specific task"""
    # First create a task
    create_response = client.post('/tasks', 
                                  json={'title': 'Get Task Test', 'description': 'Description'})
    task_id = create_response.get_json()['id']
    
    # Then get it
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Get Task Test'

def test_get_nonexistent_task(client):
    """Test getting a task that doesn't exist"""
    response = client.get('/tasks/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_update_task(client):
    """Test updating a task"""
    # Create a task
    create_response = client.post('/tasks', 
                                  json={'title': 'Original Title', 'description': 'Original Description'})
    task_id = create_response.get_json()['id']
    
    # Update it
    response = client.put(f'/tasks/{task_id}', 
                         json={'title': 'Updated Title', 'completed': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['completed'] == True

def test_delete_task(client):
    """Test deleting a task"""
    # Create a task
    create_response = client.post('/tasks', 
                                  json={'title': 'Task to Delete', 'description': 'Will be deleted'})
    task_id = create_response.get_json()['id']
    
    # Delete it
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    
    # Verify it's gone
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
```

---

### Step 5: Create Dockerfile

**File: `Dockerfile`**

```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python3", "app.py"]
```

---

### Step 6: Create Docker Compose File

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  web:
    build: .
    image: python-devsecops-jenkins_app
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

---

### Step 7: Create Jenkins Pipeline

**File: `Jenkinsfile`**

```groovy
pipeline {
    agent any
    
    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        TRIVY_IMAGE = 'aquasec/trivy:latest'
        COMPOSE_PROJECT_NAME = 'jenkins-devsecops'
        APP_PORT = '5001'  // Different port to avoid conflict with manual deployment
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        // --- Run all Python steps inside a Python container ---
        stage('Run Python Analysis & Tests') {
            agent {
                dockerContainer { 
                    image env.PYTHON_IMAGE
                    args '-v $WORKSPACE:/workspace -w /workspace'
                }
            }
            stages {
                stage('Install Dependencies') {
                    steps {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
                
                stage('Run Tests') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            pytest --junitxml=test-results.xml || true
                        '''
                    }
                    post {
                        always {
                            junit allowEmptyResults: true, testResults: 'test-results.xml'
                        }
                    }
                }
                
                stage('Static Code Analysis (Bandit)') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            bandit -r . -f json -o bandit-report.json || true
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                        }
                    }
                }
                
                stage('Check Dependency Vulnerabilities (Safety)') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            safety check --json --output safety-report.json || true
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'safety-report.json', allowEmptyArchive: true
                        }
                    }
                }
            }
        }
        
        // --- Cleanup existing Jenkins deployment ---
        stage('Cleanup Previous Deployment') {
            steps {
                script {
                    echo "Stopping previous Jenkins deployment..."
                    sh '''
                        docker-compose -p ${COMPOSE_PROJECT_NAME} down || true
                        
                        # Stop any container using our target port
                        CONTAINER_ON_PORT=$(docker ps --filter "publish=${APP_PORT}" -q)
                        if [ ! -z "$CONTAINER_ON_PORT" ]; then
                            echo "Stopping container on port ${APP_PORT}"
                            docker stop $CONTAINER_ON_PORT || true
                            docker rm $CONTAINER_ON_PORT || true
                        fi
                    '''
                }
            }
        }
        
        // --- Build Docker Image ---
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh '''
                        docker build -t ${IMAGE_NAME}:latest .
                        docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }
        
        // --- Scan the image using Trivy ---
        stage('Container Vulnerability Scan (Trivy)') {
            agent {
                dockerContainer { 
                    image env.TRIVY_IMAGE
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    trivy image --severity HIGH,CRITICAL \
                        --format json \
                        --output trivy-report.json \
                        ${IMAGE_NAME}:latest || true
                    
                    # Also show summary in console
                    trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:latest || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                }
            }
        }
        
        // --- Deploy Application ---
        stage('Deploy Application') {
            steps {
                script {
                    echo "Deploying application on port ${APP_PORT}..."
                    sh '''
                        # Create a temporary docker-compose file with custom port
                        cat > docker-compose.jenkins.yml <<EOF
version: '3.8'
services:
  web:
    image: ${IMAGE_NAME}:latest
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_ENV=production
EOF
                        
                        # Deploy using the custom compose file
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} up -d
                    '''
                }
            }
        }
        
        // --- Verify Deployment ---
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Verifying deployment..."
                    sh '''
                        echo "Waiting for application to start..."
                        sleep 10
                        
                        # Check if container is running
                        echo "=== Container Status ==="
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} ps
                        
                        # Check container logs
                        echo "=== Container Logs ==="
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} logs --tail=20
                        
                        # Test the application endpoint
                        echo "=== Testing Application ==="
                        curl -f http://localhost:${APP_PORT} && echo "✅ Application is responding!" || echo "⚠️  Application not responding"
                    '''
                }
            }
        }
    }
    
    // --- Post-build actions ---
    post {
        always {
            script {
                echo "==================================="
                echo "Pipeline Status: ${currentBuild.result}"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "==================================="
            }
        }
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                echo "📦 Image built: ${IMAGE_NAME}:${BUILD_NUMBER}"
                echo "🚀 Application deployed at: http://localhost:${APP_PORT}"
                echo "📊 Your existing app is still running on port 5000"
            }
        }
        failure {
            script {
                echo "❌ Pipeline failed! Cleaning up..."
                sh '''
                    docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} down || true
                '''
            }
        }
        cleanup {
            script {
                echo "🧹 Cleaning workspace..."
                cleanWs(deleteDirs: true, patterns: [[pattern: 'venv/**', type: 'INCLUDE']])
            }
        }
    }
}
```

---

### Step 8: Create README

**File: `README.md`**

```markdown
# DevSecOps Jenkins Pipeline Project

A complete DevSecOps implementation with automated CI/CD pipeline using Jenkins, Docker, and security scanning tools.

## Features

- 🐍 Python Flask REST API (Task Manager)
- 🧪 Automated testing with Pytest
- 🔒 Security scanning with Bandit and Safety
- 🐳 Containerized with Docker
- 🔍 Container vulnerability scanning with Trivy
- 🚀 Automated deployment with Jenkins
- 📊 Test reports and security artifacts

## API Endpoints

- `GET /` - API documentation
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task
- `GET /health` - Health check

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:5000
```

### Run Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Jenkins Pipeline

The pipeline includes the following stages:

1. **Checkout** - Clone repository
2. **Install Dependencies** - Set up Python virtual environment
3. **Run Tests** - Execute Pytest test suite
4. **Static Code Analysis** - Bandit security scan
5. **Dependency Vulnerabilities** - Safety check
6. **Build Docker Image** - Create container image
7. **Container Scan** - Trivy vulnerability scan
8. **Deploy** - Deploy to port 5001
9. **Verify** - Health check

## Security Scans

- **Bandit**: Static code analysis for Python security issues
- **Safety**: Check Python dependencies for known vulnerabilities
- **Trivy**: Container image vulnerability scanner

## Project Structure

```
.
├── app.py                 # Flask application
├── test_app.py           # Pytest tests
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose config
├── Jenkinsfile         # Jenkins pipeline
└── README.md           # This file
```

## Ports

- `5000` - Manual deployment
- `5001` - Jenkins deployment
- `8081` - Jenkins UI

## License

MIT License
```

---

### Step 9: Setup Jenkins

#### 9.1 Run Jenkins Container

```bash
# Pull and run Jenkins with Docker support
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk11

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### 9.2 Configure Jenkins

1. **Access Jenkins**: Open `http://localhost:8081`
2. **Unlock Jenkins**: Use the initial admin password from above
3. **Install Suggested Plugins**: Click "Install suggested plugins"
4. **Create Admin User**: Set up your admin credentials
5. **Configure Jenkins URL**: Set to `http://localhost:8081`

#### 9.3 Install Required Plugins

Go to **Manage Jenkins** → **Manage Plugins** → **Available** and install:

- Docker Pipeline
- Docker plugin
- Git plugin
- Pipeline plugin
- JUnit plugin
- HTML Publisher plugin

#### 9.4 Configure Docker in Jenkins

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Add Docker installation (if not auto-detected)
3. Save configuration

#### 9.5 Grant Jenkins Docker Access

```bash
# Enter Jenkins container
docker exec -it jenkins bash

# Add jenkins user to docker group (if needed)
# This is usually not needed if docker.sock is mounted correctly

# Exit container
exit
```

---

### Step 10: Push Code to GitHub

#### 10.1 Create .gitignore

**File: `.gitignore`**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
test-results.xml
*.log

# Security Reports
bandit-report.json
safety-report.json
trivy-report.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# Docker
docker-compose.jenkins.yml

# OS
.DS_Store
Thumbs.db
```

#### 10.2 Initialize and Push

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: DevSecOps Jenkins Pipeline"

# Create repository on GitHub (use GitHub web interface)
# Then add remote and push
git remote add origin https://github.com/YOUR_USERNAME/jenkinsrepo.git
git branch -M main
git push -u origin main
```

---

### Step 11: Create Jenkins Pipeline Job

#### 11.1 Create New Pipeline

1. Go to Jenkins Dashboard
2. Click **New Item**
3. Enter name: `devsecops-pipeline`
4. Select **Pipeline**
5. Click **OK**

#### 11.2 Configure Pipeline

**General Settings:**
- Description: `DevSecOps CI/CD Pipeline with Security Scans`

**Pipeline Configuration:**
1. Definition: **Pipeline script from SCM**
2. SCM: **Git**
3. Repository URL: `https://github.com/YOUR_USERNAME/jenkinsrepo.git`
4. Credentials: Add your GitHub credentials if repository is private
5. Branch: `*/main`
6. Script Path: `Jenkinsfile`

**Build Triggers (Optional):**
- ☑️ GitHub hook trigger for GITScm polling
- ☑️ Poll SCM: `H/5 * * * *` (every 5 minutes)

#### 11.3 Save and Build

1. Click **Save**
2. Click **Build Now**
3. Monitor the build in **Console Output**

---

### Step 12: Configure GitHub Webhook (Optional)

For automatic builds on push:

1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. Payload URL: `http://YOUR_JENKINS_URL:8081/github-webhook/`
4. Content type: `application/json`
5. Events: **Just the push event**
6. Click **Add webhook**

---

## Testing & Verification

### Test the Pipeline

#### 1. Manual Build Test

```bash
# Trigger a manual build in Jenkins
# Watch the Console Output for each stage
```

#### 2. Verify Each Stage

**Checkout:**
```bash
# Should clone the repository successfully
```

**Install Dependencies:**
```bash
# Should create venv and install packages
```

**Run Tests:**
```bash
# Should execute all pytest tests
# Check for test-results.xml in artifacts
```

**Static Code Analysis:**
```bash
# Should run Bandit scan
# Check bandit-report.json in artifacts
```

**Dependency Vulnerabilities:**
```bash
# Should run Safety check
# Check safety-report.json in artifacts
```

**Build Docker Image:**
```bash
# Verify image was built
docker images | grep python-devsecops-jenkins_app
```

**Container Vulnerability Scan:**
```bash
# Should scan with Trivy
# Check trivy-report.json in artifacts
```

**Deploy Application:**
```bash
# Should deploy on port 5001
docker ps | grep jenkins-devsecops
```

**Verify Deployment:**
```bash
# Test the deployed application
curl http://localhost:5001
curl http://localhost:5001/health
curl http://localhost:5001/tasks
```

### Test the Application API

#### Create a Task
```bash
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Testing the API"}'
```

#### Get All Tasks
```bash
curl http://localhost:5001/tasks
```

#### Get Specific Task
```bash
curl http://localhost:5001/tasks/1
```

#### Update Task
```bash
curl -X PUT http://localhost:5001/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "completed": true}'
```

#### Delete Task
```bash
curl -X DELETE http://localhost:5001/tasks/1
```

### View Jenkins Artifacts

1. Go to the build page in Jenkins
2. Click on the build number
3. Click **Artifacts** to download:
   - `test-results.xml` - Test results
   - `bandit-report.json` - Security scan results
   - `safety-report.json` - Dependency vulnerabilities
   - `trivy-report.json` - Container vulnerabilities

### Check Container Status

```bash
# View all running containers
docker ps

# View Jenkins deployment
docker-compose -f docker-compose.jenkins.yml -p jenkins-devsecops ps

# View logs
docker logs jenkins-devsecops_web_1

# View resource usage
docker stats jenkins-devsecops_web_1
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Jenkins Can't Access Docker

**Symptom:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Make sure docker.sock is mounted correctly
docker run -d \
  --name jenkins \
  -p 8081:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --user root \
  jenkins/jenkins:lts-jdk11
```

#### Issue 2: Port Already in Use

**Symptom:**
```
Bind for 0.0.0.0:5001 failed: port is already allocated
```

**Solution:**
```bash
# Find and stop the container using the port
docker ps --filter "publish=5001" -q | xargs docker stop

# Or change APP_PORT in Jenkinsfile
APP_PORT = '5002'
```

#### Issue 3: Python Tests Fail

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure requirements.txt is correct
# Verify virtual environment is activated in pipeline
. venv/bin/activate
```

#### Issue 4: Docker Build Fails

**Symptom:**
```
ERROR: failed to solve: failed to compute cache key
```

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t python-devsecops-jenkins_app:latest .
```

#### Issue 5: Trivy Scan Fails

**Symptom:**
```
FATAL: error connecting to Docker daemon
```

**Solution:**
```groovy
// Ensure Docker socket is mounted in Jenkinsfile
agent {
    dockerContainer { 
        image env.TRIVY_IMAGE
        args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
}
```

#### Issue 6: GitHub Webhook Not Triggering

**Solution:**
1. Check webhook delivery in GitHub Settings → Webhooks
2. Ensure Jenkins URL is accessible from internet
3. Verify webhook secret matches Jenkins configuration
4. Check Jenkins logs for webhook events

#### Issue 7: Pipeline Syntax Errors

**Symptom:**
```
Invalid agent type "docker" specified
```

**Solution:**
```groovy
// Use dockerContainer instead of docker
agent {
    dockerContainer { image 'python:3.9-slim' }
}
```

#### Issue 8: Workspace Cleanup Issues

**Symptom:**
```
Unable to delete workspace
```

**Solution:**
```groovy
// Use patterns in cleanWs
cleanWs(deleteDirs: true, patterns: [[pattern: 'venv/**', type: 'INCLUDE']])
```

---

## Best Practices

### Security Best Practices

1. **Use specific image versions** instead of `latest`
   ```groovy
   PYTHON_IMAGE = 'python:3.9.18-slim'
   ```

2. **Scan all dependencies** before deployment
   ```bash
   pip install safety
   safety check
   ```

3. **Use non-root users** in Docker
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

4. **Keep secrets secure** - Use Jenkins credentials
   ```groovy
   withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
       sh 'echo $API_KEY'
   }
   ```

5. **Regular updates** - Keep all tools and dependencies updated

### Pipeline Best Practices

1. **Use declarative pipeline** syntax (as shown)
2. **Fail fast** - Stop on critical security issues
3. **Parallel execution** - Run independent stages in parallel
4. **Artifact retention** - Keep important reports
5. **Clean workspace** - Remove temporary files

### Docker Best Practices

1. **Multi-stage builds** - Reduce image size
2. **Layer caching** - Order Dockerfile commands efficiently
3. **Health checks** - Add Docker health checks
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost:5000/health || exit 1
   ```
4. **Resource limits** - Set memory and CPU limits
5. **Use .dockerignore** - Exclude unnecessary files

---

## Advanced Configurations

### Add Slack Notifications

```groovy
post {
    success {
        slackSend(
            color: 'good',
            message: "Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded!"
        )
    }
    failure {
        slackSend(
            color: 'danger',
            message: "Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} failed!"
        )
    }
}
```

### Add Email Notifications

```groovy
post {
    always {
        emailext(
            subject: "Build ${env.BUILD_NUMBER} - ${currentBuild.result}",
            body: "Check console output at ${env.BUILD_URL}",
            to: 'team@example.com'
        )
    }
}
```

### Add SonarQube Analysis

```groovy
stage('SonarQube Analysis') {
    steps {
        script {
            def scannerHome = tool 'SonarQube Scanner'
            withSonarQubeEnv('SonarQube') {
                sh "${scannerHome}/bin/sonar-scanner"
            }
        }
    }
}
```

### Add Docker Registry Push

```groovy
stage('Push to Registry') {
    steps {
        script {
            docker.withRegistry('https://registry.hub.docker.com', 'docker-credentials') {
                def app = docker.build("${IMAGE_NAME}:${BUILD_NUMBER}")
                app.push()
                app.push('latest')
            }
        }
    }
}
```

---

## Monitoring and Maintenance

### Monitor Jenkins

```bash
# Check Jenkins logs
docker logs -f jenkins

# Check disk usage
docker exec jenkins df -h

# Check memory usage
docker stats jenkins
```

### Monitor Application

```bash
# Check application logs
docker logs -f jenkins-devsecops_web_1

# Monitor health endpoint
watch -n 5 curl http://localhost:5001/health

# Check response times
time curl http://localhost:5001/tasks
```

### Backup Jenkins

```bash
# Backup Jenkins home directory
docker exec jenkins tar czf /tmp/jenkins-backup.tar.gz /var/jenkins_home

# Copy backup to host
docker cp jenkins:/tmp/jenkins-backup.tar.gz ./jenkins-backup.tar.gz
```

### Cleanup Resources

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup (careful!)
docker system prune -a --volumes
```

---

## Performance Optimization

### Optimize Docker Builds

1. **Use BuildKit**
   ```bash
   export DOCKER_BUILDKIT=1
   docker build -t myapp .
   ```

2. **Multi-stage builds**
   ```dockerfile
   FROM python:3.9-slim as builder
   # Build dependencies
   
   FROM python:3.9-slim
   COPY --from=builder /app /app
   ```

3. **Cache pip packages**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.cache/pip \
       pip install -r requirements.txt
   ```

### Optimize Pipeline

1. **Parallel stages**
   ```groovy
   parallel {
       stage('Test') { ... }
       stage('Lint') { ... }
   }
   ```

2. **Cache dependencies**
   ```groovy
   options {
       buildDiscarder(logRotator(numToKeepStr: '10'))
       skipDefaultCheckout()
   }
   ```

3. **Use stashing**
   ```groovy
   stash name: 'built-app', includes: 'dist/**'
   unstash 'built-app'
   ```

---

## Additional Resources

### Documentation Links

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

### Useful Commands

```bash
# Jenkins
docker logs jenkins -f                    # Follow Jenkins logs
docker exec -it jenkins bash              # Enter Jenkins container
docker restart jenkins                    # Restart Jenkins

# Application
docker-compose logs -f                    # Follow app logs
docker-compose restart                    # Restart application
docker-compose down -v                    # Remove everything including volumes

# Docker
docker ps -a                              # List all containers
docker images                             # List all images
docker system df                          # Show disk usage
docker inspect <container>                # Inspect container details

# Testing
pytest -v                                 # Verbose test output
pytest --cov=app --cov-report=html       # Coverage report
bandit -r . -ll                          # Low and high severity only
safety check --full-report               # Full vulnerability report
```

---

## Conclusion

You now have a complete DevSecOps pipeline implementation with:

✅ Automated testing
✅ Security scanning at multiple levels
✅ Containerized deployment
✅ Continuous Integration/Continuous Deployment
✅ Comprehensive monitoring and reporting

### Next Steps

1. **Customize** the application for your needs
2. **Add more tests** to increase coverage
3. **Integrate** with more security tools
4. **Deploy** to production environment (Kubernetes, AWS, etc.)
5. **Monitor** in production with APM tools
6. **Iterate** and improve based on metrics

### Support

For issues or questions:
- Check the Troubleshooting section
- Review Jenkins console output
- Check Docker logs
- Consult official documentation

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Author:** DevSecOps Team  

---

## Appendix

### Full File Listing

```
jenkins-devsecops-project/
├── .gitignore
├── README.md
├── Jenkinsfile
├── Dockerfile
├── docker-compose.yml
├── app.py
├── test_app.py
└── requirements.txt
```

### Environment Variables Reference

```bash
# Jenkins Pipeline Environment Variables
PYTHON_IMAGE          # Python Docker image
IMAGE_NAME            # Application image name
TRIVY_IMAGE          # Trivy scanner image
COMPOSE_PROJECT_NAME  # Docker Compose project name
APP_PORT             # Application port
BUILD_NUMBER         # Jenkins build number
WORKSPACE            # Jenkins workspace path
JOB_NAME             # Jenkins job name
BUILD_URL            # Jenkins build URL
```

### Quick Reference Card

| Task | Command |
|------|---------|
| Start Jenkins | `docker start jenkins` |
| Stop Jenkins | `docker stop jenkins` |
| View Jenkins logs | `docker logs jenkins -f` |
| Access Jenkins | `http://localhost:8081` |
| Start app (manual) | `docker-compose up -d` |
| Stop app (manual) | `docker-compose down` |
| View app (Jenkins) | `http://localhost:5001` |
| View app (manual) | `http://localhost:5000` |
| Run tests | `pytest` |
| Security scan | `bandit -r .` |
| Build image | `docker build -t app .` |
| View containers | `docker ps` |
| View images | `docker images` |
| Clean Docker | `docker system prune -a` |

---

**End of Guide**
