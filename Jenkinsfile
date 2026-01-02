pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git(
                    branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/naila-rizvan/ci-cd-secure.git'
                )

            }
        }

        stage('SAST - Semgrep') {
            steps {
                bat '''
                docker run --rm ^
                -v "%cd%:/src" ^
                returntocorp/semgrep semgrep scan --config=auto --verbose
                '''
            }
        }

        stage('Dependency Scan - Trivy') {
            steps {
                bat 'docker run --rm -v %cd%:/project aquasec/trivy fs /project'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t secure-app .'
            }
        }

        stage('Create Docker Network') {
            steps {
                bat 'docker network inspect zap-net >nul 2>&1 || docker network create zap-net'
            }
        }

        stage('Run Application') {
            steps {
                bat '''
                docker rm -f secure-app-container || exit 0
                docker run -d --name secure-app-container ^
                --network zap-net ^
                -p 5050:5050 secure-app
                '''
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                bat '''
                docker run --rm ^
                --network zap-net ^
                -v "%cd%:/zap/wrk" ^
                zaproxy/zap-stable zap-baseline.py ^
                -t http://secure-app-container:5050 ^
                -r zap-report.html
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished'
        }
    }
}
