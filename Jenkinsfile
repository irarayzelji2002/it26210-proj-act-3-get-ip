pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    stages {
        stage('Print Workspace') {
            steps {
                echo "Workspace Directory: ${env.WORKSPACE}"
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    // Check if the repository exists
                    if (!fileExists("${env.WORKSPACE}/.git")) {
                        echo "Repository not cloned. Cloning now..."
                        bat 'git clone https://github.com/irarayzelji2002/it26210-proj-act-3-get-ip.git'
                    } else {
                        // Check if there are any new commits by fetching from the remote
                        echo "Repository already exists. Checking for new commits..."
                        bat 'git fetch --dry-run origin main'  // Dry run fetch to see if changes exist
                        def changesAvailable = bat(script: 'git rev-list --count HEAD...origin/main', returnStdout: true).trim()
                        if (changesAvailable != '0') {
                            echo "New commits found. Pulling changes..."
                            bat 'git pull origin main'  // Pull the latest changes
                        } else {
                            echo "No new commits. Skipping pull."
                        }
                    }
                }
            }
        }

        stage('Check for Changes in requirements.txt') {
            steps {
                script {
                    // Check if requirements.txt has been modified
                    def changes = bat(script: "git diff --name-only origin/main...HEAD", returnStdout: true).trim()
                    if (changes.contains("requirements.txt")) {
                        env.REINSTALL_REQUIREMENTS = "true"
                    } else {
                        env.REINSTALL_REQUIREMENTS = "false"
                    }
                    echo "Changes in requirements.txt: ${env.REINSTALL_REQUIREMENTS}"
                }
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    if (env.REINSTALL_REQUIREMENTS == "true") {
                        echo "Reinstalling dependencies..."
                        // Set up the virtual environment and install dependencies
                        bat 'python -m venv $VENV_DIR'
                        bat 'call $VENV_DIR\\Scripts\\activate.bat && pip install -r requirements.txt'
                    } else {
                        echo "Skipping installation, dependencies are already installed."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Check for changes in the repository (use bat for Windows)
                    def testChanges = bat(script: "git diff --name-only origin/main...HEAD", returnStdout: true).trim()
                    if (testChanges) {
                        echo "Changes detected, running tests..."
                        
                        // Activate virtual environment and run Nox
                        bat '''
                            call $VENV_DIR\\Scripts\\activate.bat
                            where nox
                            nox
                        '''
                    } else {
                        echo "No changes in code, skipping tests."
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'nox_output/*', allowEmptyArchive: true
        }
        success {
            echo 'Tests passed!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}
