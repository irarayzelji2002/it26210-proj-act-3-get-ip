import nox

@nox.session
def tests(session):
    # Install dependencies
    session.install("-r", "requirements.txt")
    
    # Run tests
    session.run("python", "-m", "unittest", "discover", "-s", "test", "-p", "*.py")