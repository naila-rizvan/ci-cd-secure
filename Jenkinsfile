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
                sh '''
                pip install semgrep
                semgrep --config=auto .
                '''
            }
        }

        stage('Dependency Scan - Trivy') {
            steps {
                sh '''
                docker run --rm -v ${PWD}:/project aquasec/trivy fs /project
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t secure-app .'
            }
        }

        stage('Run Application') {
            steps {
                sh 'docker run -d -p 5000:5000 --name secure-app-container secure-app'
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                sh '''
                docker run --rm -t owasp/zap2docker-stable zap-baseline.py \
                -t http://host.docker.internal:5000
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
