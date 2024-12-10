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
                        git branch: 'main', url: 'https://github.com/irarayzelji2002/it26210-proj-act-3-get-ip.git'
                    } else {
                        // Check if there are any new commits by fetching from the remote
                        echo "Repository already exists. Checking for new commits..."
                        sh 'git fetch --dry-run origin main'  // Dry run fetch to see if changes exist
                        def changesAvailable = sh(script: 'git rev-list --count HEAD...origin/main', returnStdout: true).trim()
                        if (changesAvailable != '0') {
                            echo "New commits found. Pulling changes..."
                            sh 'git pull origin main'  // Pull the latest changes
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
                    def changes = sh(script: "git diff --name-only origin/main...HEAD", returnStdout: true).trim()
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
                        sh 'python -m venv $VENV_DIR'
                        sh 'source $VENV_DIR/Scripts/activate && pip install -r requirements.txt'
                    } else {
                        echo "Skipping installation, dependencies are already installed."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run Nox only if necessary
                    def testChanges = sh(script: "git diff --name-only origin/main...HEAD", returnStdout: true).trim()
                    if (testChanges) {
                        echo "Changes detected, running tests..."
                        sh 'nox'
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
