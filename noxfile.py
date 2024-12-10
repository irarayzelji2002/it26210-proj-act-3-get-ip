import nox
import subprocess

@nox.session
def tests(session):
    # Check if the requirements are already installed
    def is_requirements_installed():
        try:
            # Check if the required packages are installed
            installed_packages = subprocess.check_output(
                [session.python, "-m", "pip", "freeze"]
            ).decode("utf-8")
            # Check if the required packages are listed in the installed packages
            with open("requirements.txt", "r") as f:
                required_packages = f.read()
                for package in required_packages.splitlines():
                    if package not in installed_packages:
                        return False
            return True
        except subprocess.CalledProcessError:
            return False

    # Install dependencies only if they're not already installed
    if not is_requirements_installed():
        session.install("-r", "requirements.txt")
    else:
        session.log("Dependencies already installed. Skipping installation.")

    # Run tests
    session.run("python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py")
