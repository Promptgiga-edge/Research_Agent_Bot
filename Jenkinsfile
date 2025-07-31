pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from the repository
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    // Install dependencies
                    sh 'python -m venv venv'
                    sh 'source venv/bin/activate && pip install --upgrade pip'
                    sh 'source venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Run unit tests
                    sh 'source venv/bin/activate && pytest tests'
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    // Perform health check
                    sh 'source venv/bin/activate && python health_check.py'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Launch the application
                    sh 'source venv/bin/activate && streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none'
                }
            }
        }
    }

    post {
        always {
            // Clean up
            cleanWs()
        }
    }
}