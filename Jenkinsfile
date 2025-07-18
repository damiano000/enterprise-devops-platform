pipeline {
    agent any

    environment {
        IMAGE_NAME = 'damianomirante/vops-microservice'
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Unit Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                }
            }
            steps {
                dir('microservice-python') {
                    sh 'pip install --no-cache-dir --root-user-action=ignore -r requirements.txt'
                    sh 'pytest test_app.py'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                dir('microservice-python') {
                    script {
                        def tag = "v${env.BUILD_NUMBER}"
                        sh "docker build -t ${env.IMAGE_NAME}:${tag} ."
                        sh "docker tag ${env.IMAGE_NAME}:${tag} ${env.IMAGE_NAME}:latest"
                        env.DOCKER_TAG = tag
                    }
                }
            }
        }
        stage('Push Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_NAME}:${DOCKER_TAG}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'microservice-python/*.py', allowEmptyArchive: true
                junit 'microservice-python/*.xml'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
