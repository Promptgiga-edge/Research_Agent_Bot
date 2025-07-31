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
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\activate.bat && pip install --upgrade pip'
                    bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Run unit tests
                    bat 'venv\\Scripts\\activate.bat && pytest tests'
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    // Perform health check
                    bat 'venv\\Scripts\\activate.bat && python health_check.py'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Launch the application
                    bat 'venv\\Scripts\\activate.bat && streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none'
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
