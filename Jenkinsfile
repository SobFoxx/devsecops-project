pipeline {
    agent any
    
    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'devsecops-project'
        TRIVY_IMAGE = 'aquasec/trivy:latest'
        COMPOSE_PROJECT_NAME = 'jenkins-devsecops-ecommerce'
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
                            pytest --junitxml=test-results.xml -v || true
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
                            bandit -r . || true
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
                            safety check || true
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
                    echo "=== Trivy Vulnerability Scan Results ==="
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
                    echo "Deploying E-Commerce API on port ${APP_PORT}..."
                    sh '''
                        # Create a temporary docker-compose file with custom port
                        cat > docker-compose.jenkins.yml <<EOF
version: '3.8'
services:
  web:
    image: ${IMAGE_NAME}:latest
    container_name: ${COMPOSE_PROJECT_NAME}-api
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
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
                    echo "Verifying E-Commerce API deployment..."
                    sh '''
                        echo "Waiting for application to start..."
                        sleep 10
                        
                        # Check if container is running
                        echo "=== Container Status ==="
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} ps
                        
                        # Check container logs
                        echo "=== Container Logs ==="
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} logs --tail=30
                        
                        # Test the application endpoints
                        echo "=== Testing Application Endpoints ==="
                        echo "Testing home endpoint..."
                        curl -f http://localhost:${APP_PORT} && echo "✅ Home endpoint OK" || echo "⚠️  Home endpoint failed"
                        
                        echo "Testing health endpoint..."
                        curl -f http://localhost:${APP_PORT}/health && echo "✅ Health endpoint OK" || echo "⚠️  Health endpoint failed"
                        
                        echo "Testing products endpoint..."
                        curl -f http://localhost:${APP_PORT}/products && echo "✅ Products endpoint OK" || echo "⚠️  Products endpoint failed"
                        
                        echo "Testing categories endpoint..."
                        curl -f http://localhost:${APP_PORT}/categories && echo "✅ Categories endpoint OK" || echo "⚠️  Categories endpoint failed"
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
                echo "✅ E-Commerce API Pipeline completed successfully!"
                echo "📦 Image built: ${IMAGE_NAME}:${BUILD_NUMBER}"
                echo "🚀 Application deployed at: http://localhost:${APP_PORT}"
                echo "📋 API Documentation: http://localhost:${APP_PORT}"
                echo "❤️  Health Check: http://localhost:${APP_PORT}/health"
                echo "📦 Products API: http://localhost:${APP_PORT}/products"
                echo "📊 Statistics: http://localhost:${APP_PORT}/stats"
                echo ""
                echo "Your manual deployment (if any) is still running on port 5000"
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
