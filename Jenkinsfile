pipeline {
    agent any

    triggers {
        GenericTrigger(
            genericVariables: [[key: 'message', value: '$.message']],
            causeString: 'Triggered on ArgoCD Sync: $message',
            token: 'CANARYTOKEN',
            printContributedVariables: true,
            printPostContent: true
        )
    }

    environment {
        IMAGE_NAME = 'damiano000/vops-microservice'
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        BACKUP_ON_S3 = 'false'
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
                    args '-u root' // Run as root to avoid permission issues
                    reuseNode true // Reuse the node for subsequent stages
                }
            }
            steps {
                dir('microservice-python') {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                    sh 'pytest --junitxml=results.xml'
                }
            }
        }
        stage('Local Artifact Backup') {
            steps {
                dir('microservice-python') {
                    sh 'mkdir -p backup'
                    sh 'cp results.xml backup/results.xml'
                    sh 'cp *.py backup/'
                }
            }
        }
        stage('Backup Test Report on S3') {
            when {
                expression { env.BACKUP_ON_S3 == 'true' }
            }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-devops-creds']]) {
                    dir('microservice-python') {
                        sh ' aws s3 cp results.xml s3://vops-logs-fc4f455f/results-latest.xml'
                    }
                }
            }
        }
        stage('Validate K8s Manifest') {
            steps {
                    sh 'kubeval k8s/dev/*.yaml'
                    sh 'kubeval k8s/prod/*.yaml'
            }
        }
        stage('Build Docker Image') {
            when {
                branch 'main'
            }
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
            when {
                branch 'main'
            }
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
                junit 'microservice-python/results.xml'
                archiveArtifacts artifacts: 'microservice-python/backup/*', allowEmptyArchive: true
            }
        }
        stage('Canary Test') {
            when {
                allOf {
                    branch 'main'
                    expression { return env.message != null }
                }
            }
            steps {
                echo "Running canary test after ArgoCD Sync: ${env.message}"
                sh './tests/test_canary_routing.sh'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
