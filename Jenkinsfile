pipeline {
    agent none

    stages {

        stage('Build Docker Image') {
            agent { label 'docker' }
            steps {

                sh '''
                    echo "Harbor12345" | docker login 192.168.1.10:8083 --username "admin" --password-stdin

                    docker build -t email-service:latest .

                    docker tag email-service:latest 192.168.1.10:8083/library/email-service:latest
                    docker push 192.168.1.10:8083/library/email-service:latest
                '''

            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'kubectl' }
            steps {
                withCredentials([file(credentialsId: 'kubectl-config', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl --context kind-library apply -f deployment.yml --validate=false
                        kubectl --context kind-library apply -f service.yml
                        kubectl --context kind-library rollout status deployment/email-service
                    '''
                }
            }
        }
    }
}