pipeline {

    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod

spec:
  containers:

    - name: docker
      image: docker:26
      command:
        - cat
      tty: true

      env:
        - name: DOCKER_HOST
          value: tcp://localhost:2375


    - name: dind
      image: docker:26-dind

      securityContext:
        privileged: true

      env:
        - name: DOCKER_TLS_CERTDIR
          value: ""


    - name: git
      image: alpine/git:latest
      command:
        - cat
      tty: true
'''
        }
    }

    environment {
        IMAGE = 'hatif007/python-argo-jenkins-demo'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checkout source code'

                checkout scm
            }
        }


        stage('Docker Build') {
            steps {

                container('docker') {

                    sh '''
                        echo "Waiting for Docker daemon..."

                        until docker info >/dev/null 2>&1; do
                            sleep 1
                        done

                        echo "Docker is ready"

                        docker build \
                            -t ${IMAGE}:${BUILD_NUMBER} .

                        docker tag \
                            ${IMAGE}:${BUILD_NUMBER} \
                            ${IMAGE}:latest
                    '''
                }
            }
        }


        stage('Docker Push') {
            steps {

                container('docker') {

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {

                        sh '''
                            echo "$DOCKER_PASS" | \
                            docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin

                            docker push \
                            ${IMAGE}:${BUILD_NUMBER}

                            docker push \
                            ${IMAGE}:latest
                        '''
                    }
                }
            }
        }


       stage('Update GitOps') {
    steps {

        sh '''
            echo "Updating Kubernetes image..."

            sed -i \
            "s#image: ${IMAGE}:.*#image: ${IMAGE}:${BUILD_NUMBER}#" \
            k8s/deployment.yaml

            echo "New image:"
            grep "image:" k8s/deployment.yaml

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
    git push \
    https://${GIT_USER}:${GIT_TOKEN}@github.com/hatif007/pythonargojenkins-demo.git \
    HEAD:main
'''
        }
    }
}
    }

}