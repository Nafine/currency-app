pipeline {
    agent any

    options {
        gitLabConnection('yadro-gitlab')
    }

    environment {
        APP_VERSION = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
    }

    stages {
        stage('Lint python') {
            agent {
                docker {
                    image 'ghcr.io/astral-sh/ruff:0.15.7-alpine'
                }
            }
            steps {
                gitlabCommitStatus(name: 'lint python') {
                    sh 'ruff check .'
                }
            }
        }
        stage('Lint dockerfile') {
            when {
                expression {
                    return fileExists('Dockerfile')
                }
            }
            agent {
                docker {
                    image 'hadolint/hadolint:fcbd01791c9251d83f2486e61ecaf41ee700a766-debian-amd64'
                }
            }
            steps {
                gitlabCommitStatus(name: 'lint dockerfile') {
                    sh 'hadolint Dockerfile'
                }
            }
        }
        stage('Test') {
            when {
                expression {
                    return fileExists('main.py')
                }
            }
            agent {
                docker {
                    image 'ghcr.io/sevenbunu/devops_sandbox:0.2.0'
                    args  '-u root'
                }
            }
            steps {
                gitlabCommitStatus(name: 'test') {
                    sh 'run_tests'
                }
            }
            post {
                success {
                    junit 'report.xml'
                }
            }
        }
        stage('Build') {
            when {
                expression {
                    return fileExists('Dockerfile')
                }
            }
            agent {
                docker {
                    image 'gcr.io/kaniko-project/executor:v1.22.0-debug'
                    args '--entrypoint="" -u 0'
                }
            }
            environment {
                IMAGE_NAME = "naf1ne/currency-app:${APP_VERSION}"
            }
            steps {
                gitlabCommitStatus(name: 'build') {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            AUTH=$(echo -n "${DOCKER_USER}:${DOCKER_PASS}" | base64)
                            echo "{\\"auths\\":{\\"https://index.docker.io/v1/\\":{\\"auth\\":\\"${AUTH}\\"}}}" > /kaniko/.docker/config.json

                            /kaniko/executor \
                                --context "${WORKSPACE}" \
                                --dockerfile "${WORKSPACE}/Dockerfile" \
                                --destination "${IMAGE_NAME}"
                        '''
                    }
                }
            }
        }
        stage ('Deploy') {
            when {
                branch 'master'
            }
            agent {
                docker {
                    image 'alpine/helm:4.1.3'
                    args '--entrypoint="" -u 0'
                }
            }
            steps {
                gitlabCommitStatus(name: 'deploy') {
                    input message: "Deploy version ${APP_VERSION} to production", ok: "Deploy"
                    withCredentials([file(credentialsId: "kubeconfig", variable: 'KUBECONFIG')]) {
                        sh """
                            helm upgrade -i yadro-app ./helm/yadro-app \
                            -n yadro-app \
                            --create-namespace \
                            --rollback-on-failure \
                            --timeout 3m \
                            --set image.tag=${APP_VERSION}
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline failed'
        }
    }
}