pipeline {
    agent any

    environment {
        IMAGE = 'hatif007/python-argo-jenkins-demo'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE}:${BUILD_NUMBER} .
                    docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:latest
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push ${IMAGE}:${BUILD_NUMBER}
                        docker push ${IMAGE}:latest
                    '''
                }
            }
        }

        stage('Update GitOps') {
            steps {

                sh '''
                    sed -i \
                    "s#image: hatif007/python-argo-jenkins-demo:.*#image: hatif007/python-argo-jenkins-demo:${BUILD_NUMBER}#" \
                    k8s/deployment.yaml

                    git config user.name "jenkins"
                    git config user.email "jenkins@local"

                    git add k8s/deployment.yaml
                    git commit -m "Deploy build ${BUILD_NUMBER}" || true
                '''

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/hatif007/python-argo-jenkins-demo.git HEAD:main
                    '''
                }
            }
        }
    }
}