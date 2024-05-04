pipeline {
    agent none

    stages {
        stage ('Get code') {
            agent { label 'Agent1' } 
            steps {
                sh 'whoami'
                sh 'hostname'
                echo 'Pulling repo'
                checkout([$class: 'GitSCM', branches: [[name: '*/develop']],
                    userRemoteConfigs: [[url: 'https://github.com/dev-alex-ops/anieto-unir.git']]])
                stash includes: 'app/**/*', name: 'app'
                stash includes: 'test/**/*', name: 'test'
                stash includes: 'pytest.ini', name: 'pytest'
            }
        }

        stage('Tests') {
            parallel {
                stage ('Unit tests') {
                    agent { label 'Agent1' }
                    steps {
                        sh 'whoami'
                        sh 'hostname'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export PYTHONPATH=.
                                python3 -m pytest --junitxml=junit-unit.xml test/unit
                            '''
                        }
                    }
                }

                stage ('Service Tests') {
                    agent { label 'Agent2' }
                    steps {
                        sh 'whoami'
                        sh 'hostname'
                        unstash 'app'
                        unstash 'test'
                        unstash 'pytest'
                        sh '''
                            [ -f test/wiremock/wiremock-standalone-3.5.4.jar ] || wget https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/3.5.4/wiremock-standalone-3.5.4.jar -P test/wiremock
                            export FLASK_APP=app/api.py
                            (python3 -m flask run &)
                            sleep 1
                            (java -jar test/wiremock/wiremock-standalone-3.5.4.jar --port 9090 --root-dir test/wiremock &)
                            sleep 1
                            '''
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                            export PYTHONPATH=.
                            python3 -m pytest --junitxml=junit-rest.xml test/rest
                            '''
                        }
                        stash includes: 'junit*.xml', name: 'Rest'
                    }
                }
            }
        }

        stage('Render results') {
            agent {label 'Agent1'}
            steps{
                sh 'whoami'
                sh 'hostname'
                unstash 'Rest'
                junit 'junit*.xml'
                echo 'Done!'
            }
        }
    }
}