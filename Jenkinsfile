pipeline {
    agent any
    environment {
        PATH = "C:/Users/alsab/AppData/Local/Programs/Python/Python311;$PATH"
    }
    stages {
        stage('Get code'){
            steps {
                git url: 'https://github.com/dev-alex-ops/anieto-unir', branch: 'feature_fix_coverage'
            }
        } 

        stage ('Cobertura') {
            steps {
                bat '''
                    set PYTHONPATH=.
                    python -m coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=junit-unit.xml test\\unit
                    python -m coverage xml
                '''
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