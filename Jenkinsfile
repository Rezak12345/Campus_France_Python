pipeline {
    agent any

    environment {
        HEADLESS = 'true'
        PYTHONUTF8 = '1'  // Force Python en UTF-8
    }

    stages {

        stage('Checkout SCM') {
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
                    chcp 65001  # UTF-8 console
                    $OutputEncoding = [System.Text.Encoding]::UTF8

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
                # Ici tu peux ajouter du code pour fermer le driver si nécessaire
            """
        }
    }
}
