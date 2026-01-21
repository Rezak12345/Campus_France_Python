pipeline {
    agent any

    environment {
        HEADLESS = 'true'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                powershell """
                    python -m pip install --upgrade pip
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell """
                    pip install -r requirements.txt
                    pip install behave selenium webdriver-manager behave-html-formatter
                """
            }
        }

        stage('List Project Files') {
            steps {
                powershell """
                    Write-Output "Structure du projet :"
                    Get-ChildItem -Recurse
                """
            }
        }

        stage('Run Behave Test') {
            steps {
                powershell """
                    Write-Output "Exécution du test Behave pour Creation_etudiant.feature en mode headless"
                    behave features/Creation_etudiant.feature -f behave_html_formatter:HTMLFormatter -o report.html --no-capture -v
                """
            }
        }

        stage('Archive HTML Report') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            powershell """
                Write-Output "Nettoyage éventuel du navigateur Selenium..."
            """
        }
    }
}
