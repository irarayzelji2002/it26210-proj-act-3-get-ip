import nox
import subprocess

@nox.session
def tests(session):
    def is_requirements_installed():
        try:
            # Get the list of installed packages
            installed_packages = subprocess.check_output(
                [session.python, "-m", "pip", "freeze"], universal_newlines=True
            ).splitlines()

            # Load required packages
            with open("requirements.txt", "r") as f:
                required_packages = f.read().splitlines()

            # Ensure all required packages are installed
            for package in required_packages:
                # Check if package (ignoring version) exists in installed packages
                if not any(installed.startswith(package.split("==")[0]) for installed in installed_packages):
                    return False

            return True
        except Exception as e:
            session.error(f"Error while checking installed packages: {e}")
            return False

    # Install dependencies only if they're not already installed
    if not is_requirements_installed():
        session.install("-r", "requirements.txt")
    else:
        session.log("Dependencies already installed. Skipping installation.")

    # Run tests
    session.run("python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py")
