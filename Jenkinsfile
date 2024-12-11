pipeline {
    agent any

    environment {
        REPO_DIR = "${env.WORKSPACE}/it26210-proj-act-3-get-ip"
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
                    if (!fileExists("${env.WORKSPACE}/it26210-proj-act-3-get-ip/.git")) {
                        echo "Repository not cloned. Cloning now..."
                        bat "git clone https://github.com/irarayzelji2002/it26210-proj-act-3-get-ip.git"
                    } else {
                        // Dry run fetch to see if changes exist then pull the latest changes
                        echo "Repository already exists. Checking for new commits..."
                        bat """
                            cd ${REPO_DIR}
                            git fetch --dry-run origin main
                        """
                        def changesAvailable = bat(script: 
                        """
                            cd ${REPO_DIR}
                            git rev-list --count HEAD...origin/main
                        """, returnStdout: true).trim()
                        if (changesAvailable != '0') {
                            echo "New commits found. Pulling changes..."
                            bat """
                                cd ${REPO_DIR}
                                git pull origin main
                            """
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
                    def changes = bat(script: """
                        cd ${REPO_DIR}
                        git diff --name-only origin/main...HEAD
                    """, returnStdout: true).trim()
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
                        bat """
                            cd "${REPO_DIR}"
                            python -m venv "${REPO_DIR}\\.venv"
                        """
                        bat """
                            cd "${REPO_DIR}"
                            call "${REPO_DIR}\\.venv\\Scripts\\activate.bat" && pip install -r "${REPO_DIR}\\requirements.txt"
                        """
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
                    def testChanges = bat(script: """
                        cd "${REPO_DIR}"
                        git diff --name-only origin/main...HEAD
                    """, returnStdout: true).trim()
                    if (testChanges) {
                        echo "Changes detected, running tests..."
                        
                        // Activate virtual environment and run Nox
                        bat """
                            cd "${REPO_DIR}"
                            call "${REPO_DIR}\\.venv\\Scripts\\activate.bat"
                            where nox
                            nox
                        """
                    } else {
                        echo "No changes in code, skipping tests."
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${REPO_DIR}/nox_output/*", allowEmptyArchive: true
        }
        success {
            echo 'Tests passed!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}
