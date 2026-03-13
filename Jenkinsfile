pipeline {
    agent none

    stages {

        stage('Build Docker Image') {
            agent { label 'docker' }
            steps {
                sh 'docker build -t 192.168.1.10:5000/email-service:latest .'
                sh 'docker push 192.168.1.10:5000/email-service:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'kubectl' }
            steps {
                withCredentials([file(credentialsId: 'kubectl-config', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl --context kind-library apply -f deployment.yml
                        kubectl --context kind-library apply -f service.yml
                        kubectl --context kind-library rollout status deployment/email-service
                    '''
                }
            }
        }
    }
}