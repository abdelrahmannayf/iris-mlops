pipeline {
    agent any

    environment {
        DOCKERHUB_CRED     = credentials('dockerhub-cred')
        GITHUB_CRED        = credentials('github-cred')
        IMAGE_NAME         = "abdelrahmannayf/iris-trainer"
        IMAGE_TAG          = "${GIT_COMMIT}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                git credentialsId: 'github-cred',
                    url: 'https://github.com/abdelrahmannayf/iris-mlops.git',
                    branch: 'main'
            }
        }

        stage('Build Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh """
                    docker run --rm \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    python -c "from sklearn.datasets import load_iris; print('✅ Dependencies OK')"
                """
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Scanning with Trivy...'
                sh "trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '📤 Pushing to DockerHub...'
                sh """
                    echo ${DOCKERHUB_CRED_PSW} | \
                    docker login -u ${DOCKERHUB_CRED_USR} --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    docker push ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '☸️ Deploying to Kubernetes...'
                sshagent(['agent-ssh-key']) {
                    sh """
                        kubectl apply -f k8s/mlflow-deployment.yaml
                        kubectl apply -f k8s/prometheus-deployment.yaml
                        kubectl apply -f k8s/grafana-deployment.yaml
                        kubectl apply -f k8s/trainer-deployment.yaml
                        kubectl rollout status deployment/iris-trainer
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }
    }
}
