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

        // ----- Staging Deployment -----
        stage('Deploy to Staging') {
            steps {
                bat '''
                docker rm -f secure-app-staging || exit 0
                docker run -d --name secure-app-staging ^
                --network zap-net ^
                -p 6060:5050 secure-app
                '''
            }
        }

        // ----- DAST Scan on Staging -----
        stage('DAST - OWASP ZAP (Staging)') {
            steps {
                script {
                    def zapStatus = bat(
                        script: '''
                        docker run --rm ^
                        --network zap-net ^
                        -v "%cd%:/zap/wrk" ^
                        zaproxy/zap-stable zap-baseline.py ^
                        -t http://secure-app-staging:5050 ^
                        -r zap-staging-report.html
                        ''',
                        returnStatus: true
                    )

                    echo "ZAP exit code: ${zapStatus} (warnings are acceptable)"
                }
            }
        }


        // ----- Cleanup Staging Container -----
        stage('Cleanup Staging') {
            steps {
                bat 'docker rm -f secure-app-staging || exit 0'
            }
        }

        // ----- Optional Production Deployment -----
        stage('Deploy to Production') {
            steps {
                input message: 'Approve deployment to production?'
                bat '''
                docker rm -f secure-app-prod || exit 0
                docker run -d --name secure-app-prod ^
                -p 5080:5050 secure-app
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
