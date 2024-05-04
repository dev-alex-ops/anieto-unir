pipeline {
    agent any
    environment {
        PATH = "C:/Users/alsab/AppData/Local/Programs/Python/Python311;$PATH"
    }
    stages {
        stage('Get code'){
            steps {
                git 'https://github.com/dev-alex-ops/anieto-unir'
            }
        }
        
        stage('Build'){
            steps {
                echo 'This is Python ;)'
                bat 'dir'
            }
        }
        
        stage('Tests'){
            parallel {
                stage('Unit tests'){
                steps {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {    
                        bat '''
                            set PYTHONPATH=%WORKSPACE%
                            python -m pytest --junitxml=result-unit.xml test\\unit
                        '''
                        }
                    }
                }
            
                stage('Service tests'){
                    steps {
                        bat '''
                            set FLASK_APP=app\\api.py
                            start python -m flask run
                            start java -jar C:\\Users\\alsab\\Documents\\Wiremock\\wiremock-standalone-3.5.4.jar --port 9090 --root-dir test\\wiremock
                            
                            set PYTHONPATH=.
                            python -m pytest --junitxml=result-rest.xml test\\rest
                        '''
                    }
                }
            }
        }
        
        stage('Render Results'){
            steps{
                junit 'result*.xml'
                echo 'Done!'
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: true,
                cleanWhenAborted: true,
                cleanWhenFailure: true,
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true,
                patterns: [[pattern: '**/*', type: 'INCLUDE'],
                        [pattern: '.propsfile', type: 'EXCLUDE']])
            }
        }
    }
}
