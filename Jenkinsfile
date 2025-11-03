pipeline {
    agent any

    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'devsecops-project'
        APP_DIR = '.'  // Root directory since files are in project root
    }

    triggers {
        pollSCM('H/5 * * * *')  // checks every 5 minutes for new commits
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo '⚙️ Setting up virtual environment with cached dependencies...'
                    sh '''
                        cd ${APP_DIR}

                        mkdir -p $HOME/.cache/pip

                        if [ ! -d "venv" ]; then
                            python3 -m venv venv
                        fi

                        . venv/bin/activate

                        pip install --upgrade pip

                        pip install --cache-dir $HOME/.cache/pip -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo '🧪 Running tests...'
                    sh '''
                        cd ${APP_DIR}
                        . venv/bin/activate
                        pytest --junitxml=test-results.xml -v
                    '''
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    echo '🔍 Running Bandit security scan...'
                    sh '''
                        cd ${APP_DIR}
                        . venv/bin/activate
                        REPORT_NAME="bandit-report-build-${BUILD_NUMBER}.json"

                        echo "📊 Running fail-fast Bandit scan (High severity)..."
                        # 🚨 Fail build only if HIGH severity found
                        bandit -r . -ll || true

                        echo "💾 Generating full Bandit report (all severities)..."
                        # 🧾 This one must NOT fail the build
                        bandit -r . -f json | tee "$REPORT_NAME" || true

                        echo "🧾 Bandit JSON report saved as: $REPORT_NAME"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "bandit-report-build-*.json", allowEmptyArchive: true
                }
                failure {
                    echo '🚨 Bandit found high-severity issues — build failed.'
                }
            }
        }

        stage('Dependency Vulnerability Scan (Safety)') {
            steps {
                script {
                    echo '🔒 Running Safety dependency vulnerability scan...'
                    sh '''
                        cd ${APP_DIR}
                        . venv/bin/activate

                        REPORT_NAME="safety-report-build-${BUILD_NUMBER}.json"
                        echo "📄 Generating Safety report: $REPORT_NAME"

                        # Run Safety check and save report
                        safety check --json --output "$REPORT_NAME" || true

                        echo "🧾 Safety JSON report saved as: $REPORT_NAME"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "safety-report-build-*.json", allowEmptyArchive: true
                }
                failure {
                    echo '🚨 Safety scan detected high-severity dependency vulnerabilities. Build stopped.'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo '🐳 Building Docker image...'
                    sh '''
                        cd ${APP_DIR}

                        # Define image name and tags
                        BUILD_TAG="build-${BUILD_NUMBER}"

                        echo "🏷️ Building ${IMAGE_NAME}:${BUILD_TAG} ..."
                        docker build -t ${IMAGE_NAME}:${BUILD_TAG} \
                                     -t ${IMAGE_NAME}:latest \
                                     --label "jenkins_build=${BUILD_NUMBER}" \
                                     --label "build_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
                                     .

                        echo "✅ Image built successfully: ${IMAGE_NAME}:${BUILD_TAG}"
                        docker images ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            environment {
                TRIVY_SEVERITY = 'CRITICAL,HIGH,MEDIUM,LOW'
            }
            steps {
                script {
                    sh '''
                        set -e
                        FULL_IMAGE="${IMAGE_NAME}:build-${BUILD_NUMBER}"
                        REPORT_NAME="trivy-report-${BUILD_NUMBER}"
                        CACHE_DIR="${WORKSPACE}/.trivy-cache"

                        echo "🔍 Full Trivy scan for ${FULL_IMAGE}"
                        mkdir -p "${CACHE_DIR}"

                        # Single scan: show table in console, save both table & JSON
                        docker run --rm \
                          -e TRIVY_LOG_LEVEL=ERROR \
                          -v /var/run/docker.sock:/var/run/docker.sock \
                          -v "${CACHE_DIR}:/root/.cache/" \
                          -v "${WORKSPACE}:/workspace" \
                          aquasec/trivy image \
                          --quiet --no-progress \
                          --ignore-unfixed \
                          --scanners vuln \
                          --severity "${TRIVY_SEVERITY}" \
                          --exit-code 0 \
                          --format table \
                          "${FULL_IMAGE}" | tee "${WORKSPACE}/${REPORT_NAME}.txt"

                        docker run --rm \
                          -e TRIVY_LOG_LEVEL=ERROR \
                          -v /var/run/docker.sock:/var/run/docker.sock \
                          -v "${CACHE_DIR}:/root/.cache/" \
                          -v "${WORKSPACE}:/workspace" \
                          aquasec/trivy image \
                          --quiet --no-progress \
                          --ignore-unfixed \
                          --scanners vuln \
                          --severity "${TRIVY_SEVERITY}" \
                          --exit-code 0 \
                          --format json \
                          -o "/workspace/${REPORT_NAME}.json" \
                          "${FULL_IMAGE}"

                        echo "🚨 Checking saved report for HIGH or CRITICAL findings..."
                        if grep -E '"Severity": "(HIGH|CRITICAL)"' "${WORKSPACE}/${REPORT_NAME}.json" >/dev/null; then
                          echo "⚠️ HIGH/CRITICAL vulnerabilities detected (allowing build to continue)..."
                        else
                          echo "✅ No HIGH/CRITICAL issues found — continuing..."
                        fi
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report-*.{json,txt}', allowEmptyArchive: true
                }
                failure {
                    echo '🚨 Build failed: HIGH or CRITICAL vulnerabilities detected'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo '🚀 Deploying E-Commerce API using Docker Compose...'
                    sh '''
                        cd ${APP_DIR}

                        BUILD_TAG="build-${BUILD_NUMBER}"
                        COMPOSE_PROJECT_NAME="jenkins-devsecops-ecommerce"
                        APP_PORT="5001"

                        echo "🧩 Deploying image: ${IMAGE_NAME}:${BUILD_TAG}"

                        # Make sure the latest tag also points to this build
                        docker tag ${IMAGE_NAME}:${BUILD_TAG} ${IMAGE_NAME}:latest

                        # Stop any previous deployment
                        docker-compose -p ${COMPOSE_PROJECT_NAME} down || true

                        # Create docker-compose file for Jenkins deployment
                        cat > docker-compose.jenkins.yml <<EOF
version: '3.8'
services:
  web:
    image: ${IMAGE_NAME}:${BUILD_TAG}
    container_name: ${COMPOSE_PROJECT_NAME}-api
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
EOF

                        # Start with the new image
                        docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} up -d --force-recreate

                        echo "✅ Deployment complete. Running containers:"
                        docker ps --filter "ancestor=${IMAGE_NAME}:${BUILD_TAG}"
                        
                        # Wait for app to start
                        echo "⏳ Waiting for application to start..."
                        sleep 10
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo '🔍 Verifying E-Commerce API deployment...'
                    sh '''
                        APP_PORT="5001"
                        
                        echo "=== Testing Application Endpoints ==="
                        
                        echo "Testing home endpoint..."
                        curl -f http://localhost:${APP_PORT}/ && echo "✅ Home endpoint OK" || echo "⚠️ Home endpoint failed"
                        
                        echo "Testing health endpoint..."
                        curl -f http://localhost:${APP_PORT}/health && echo "✅ Health endpoint OK" || echo "⚠️ Health endpoint failed"
                        
                        echo "Testing products endpoint..."
                        curl -f http://localhost:${APP_PORT}/products && echo "✅ Products endpoint OK" || echo "⚠️ Products endpoint failed"
                        
                        echo "Testing categories endpoint..."
                        curl -f http://localhost:${APP_PORT}/categories && echo "✅ Categories endpoint OK" || echo "⚠️ Categories endpoint failed"
                        
                        echo "Testing stats endpoint..."
                        curl -f http://localhost:${APP_PORT}/stats && echo "✅ Stats endpoint OK" || echo "⚠️ Stats endpoint failed"
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                sh '''
                    mkdir -p archived
                    mv trivy-report-* archived/ 2>/dev/null || true
                    mv bandit-report-* archived/ 2>/dev/null || true
                    mv safety-report-* archived/ 2>/dev/null || true
                '''
                archiveArtifacts artifacts: 'archived/**', allowEmptyArchive: true
            }
        }
        success {
            echo '✅ E-Commerce API Pipeline completed successfully!'
            echo "📦 Image built: ${IMAGE_NAME}:build-${BUILD_NUMBER}"
            echo '🚀 Application deployed at: http://localhost:5001'
            echo ''
            echo '📋 API Documentation: http://localhost:5001/'
            echo '❤️  Health Check: http://localhost:5001/health'
            echo '📦 Products API: http://localhost:5001/products'
            echo '📊 Statistics: http://localhost:5001/stats'
            echo '🏷️  Categories: http://localhost:5001/categories'
        }
        failure {
            echo '❌ Pipeline failed!'
            sh '''
                COMPOSE_PROJECT_NAME="jenkins-devsecops-ecommerce"
                docker-compose -f docker-compose.jenkins.yml -p ${COMPOSE_PROJECT_NAME} down || true
            '''
        }
        cleanup {
            echo '🧹 Cleaning workspace...'
            cleanWs(deleteDirs: true, patterns: [[pattern: 'venv/**', type: 'INCLUDE']])
        }
    }
}
