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
                returntocorp/semgrep semgrep scan --config=auto
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

        stage('Run Application') {
            steps {
                bat 'docker run -d -p 5000:5000 --name secure-app-container secure-app'
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                bat '''
                docker run --rm -t owasp/zap2docker-stable ^
                zap-baseline.py -t http://host.docker.internal:5000 ^
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
