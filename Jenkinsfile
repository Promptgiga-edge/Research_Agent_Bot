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
                    // Check Python installation and install dependencies
                    bat '''
                        echo cd
                        echo Checking Python installation...
                        set PYTHON_PATH=C:\\Users\\bipla\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe
                        %PYTHON_PATH% --version
                        
                        echo Creating virtual environment...
                        %PYTHON_PATH% -m venv .venv
                        
                        echo Activating virtual environment and installing dependencies...
                        call .venv\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Run unit tests
                    bat '''
                        call .venv\\Scripts\\activate.bat
                        pytest tests || echo "Tests completed with exit code %ERRORLEVEL%"
                    '''
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    // Perform health check
                    bat '''
                        call .venv\\Scripts\\activate.bat
                        python health_check.py || echo "Health check completed with exit code %ERRORLEVEL%"
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Launch the application
                    bat '''
                        call .venv\\Scripts\\activate.bat
                        echo Starting Streamlit application...
                        streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none
                    '''
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
