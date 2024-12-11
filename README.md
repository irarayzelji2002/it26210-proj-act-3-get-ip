# IT26210 - IP Info Getter Application

### Project Activity 3 - Social Coding | Project Activity 4 - Automated Software Testing and Deployment

IT26210 - 4ITE\
1st Semester, AY 2024 - 2025

### Group Members

Del Rosario, Yna Sophia\
Esteban, Aliah DR.\
Ji, Ira Rayzel S.\
Palomo, Jakob Michael M.

## Setup Instructions

### Step 1 - Clone repository

```bash
git clone https://github.com/irarayzelji2002/it26210-proj-act-3-get-ip.git
cd it26210-proj-act-3-get-ip
git checkout main
```

### Step 2 - Setup Virtual Environment

On Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3 - Install Dependencies

```bash
pip install -r requirements.txt
deactivate
```

#### Make sure dependencies are solved and using the correct Python Interpreter.

Go to template/app.py

Ctrl+Shift+P, then select Python Interpreter in `.venv\Scripts\python.exe`

Run the app (python app.py)
If module not found, switch to your computer's Python Interpreter and switch back to `.venv\Scripts\python.exe`

```bash
npm install
```

## Updating Dependencies

On Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

This will run the app on http://127.0.0.1:8080. Press Ctrl+C to stop.

## Testing Instructions

Nox automatically creates its own virtual environments for testing, so you don't need to activate your .venv for this. If a test fails, review the error messages and ensure all dependencies are correctly installed. If you prefer to run the tests without Nox, you can still use `python -m unittest discover -s test -p "*.py"`

### Step 1 - Install Nox

Ensure Nox is installed on your system. If not, install it using pip:

```bash
pip install nox
```

### Step 2 - Run Tests

To run all tests using Nox, execute the following command:

```bash
nox
```

This will automatically set up the test environment, discover all tests in the test folder, and execute them.
