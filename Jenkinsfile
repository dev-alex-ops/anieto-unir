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
        
        stage ('Static') {
            steps {
                bat '''
                    python -m flake8 --format=pylint --exit-zero app > flake8.out
                '''
                recordIssues tools: [flake8(pattern: 'flake8.out')], qualityGates: [[threshold: 8, type: 'TOTAL', unstable: true], [threshold: 10, type: 'TOTAL', unstable: false]]
            }
        }
        
        stage ('Security') {
            steps {
                bat '''
                    python -m bandit --exit-zero -r . -f custom -o bandit.out --severity-level medium --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE'){
                    recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], [threshold: 4, type: 'TOTAL', unstable: false]]
                }
            }
        }
        
        stage ('Performance') {
            steps {
                bat '''
                    set FLASK_APP=app\\api.py
                    start python -m flask run
                    C:\\Users\\alsab\\Documents\\JMeter\\bin\\jmeter -n -t C:\\Users\\alsab\\Documents\\JMeter\\bin\\PerfPipeline.jmx -f -l flask.jtl
                '''
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
        
        stage('Tests'){
            parallel {
                stage('Unit tests'){
                steps {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {    
                        bat '''
                            set PYTHONPATH=%WORKSPACE%
                            python -m coverage run --branch --source=app --omit=app\\__init.py__,app\\api.py -m pytest --junitxml=junit-unit.xml test\\unit
                        '''
                        junit 'junit*.xml'
                        }
                    }
                }
            
                stage('Service tests'){
                    steps {
                        bat '''
                            start java -jar C:\\Users\\alsab\\Documents\\Wiremock\\wiremock-standalone-3.6.0.jar --port 9090 --root-dir test\\wiremock
                            set PYTHONPATH=.
                            python -m pytest --junitxml=result-rest.xml test\\rest
                        '''
                    }
                }
            }
        }
        
        stage ('Cobertura') {
            steps {
                bat 'python -m coverage xml'
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    cobertura coberturaReportFile: 'coverage.xml', onlyStable: false, failUnstable: false, conditionalCoverageTargets: '100,80,90', lineCoverageTargets: '100,85,95'
                }
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
