# Campus Ticket Management System

A Flask and SQLite web application for campus students to submit service requests and for administrators to track and update their status.

## Features

- Student and administrator sign-in with hashed passwords
- Student ticket submission with IT, electrical, plumbing, furniture, and other categories
- Student view of personal ticket history and status
- Administrator view of all tickets and their submitters
- Ticket workflow protection that prevents a ticket moving directly from **Pending** to **Resolved** without first entering **In Progress**
- SQLite schema initialization and sample records

## Technology stack

- Python 3
- Flask 3.0.3
- Werkzeug 3.0.3 for password hashing
- SQLite
- HTML templates with CSS
- pytest 8.2.2 for tests

## Requirements

- Python 3.9 or newer
- pip

## Setup

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, activate with `source .venv/bin/activate`.

2. Install dependencies:

   ```shell
   python -m pip install -r requirements.txt
   ```

3. (Recommended) Set a persistent Flask session key before starting the app. If `SECRET_KEY` is not set, the app generates a temporary key at startup, which signs users out whenever the process restarts.

   PowerShell:

   ```powershell
   $env:SECRET_KEY = "replace-with-a-long-random-value"
   ```

   macOS or Linux:

   ```shell
   export SECRET_KEY="replace-with-a-long-random-value"
   ```

4. Initialize the local database and sample accounts:

   ```shell
   python init_db.py
   ```

   The sample logins are `student1` / `pass123` and `admin` / `admin123`. These are development-only demo credentials. Change or remove them before using the application beyond local development.

5. Run the application:

   ```shell
   python app.py
   ```

   Open <http://127.0.0.1:5000> in your browser. Flask debug mode is enabled by the current development entry point; do not expose it to an untrusted network.

## Database

`init_db.py` creates `campus.db` in the working directory. The schema contains:

- `users`: username, password hash, and role
- `tickets`: student, title, category, and status

The database and its backups are excluded from Git. Running the initializer creates sample records only when the users table is empty.

## Tests

Run the test suite with:

```shell
python -m pytest
```

## Project layout

```text
app.py                      Flask routes and application entry point
db.py                       SQLite schema, sample data, and data access
init_db.py                  Database initialization command
test_app.py                 Authentication and ticket workflow tests
requirements.txt            Python dependencies
templates/                  Login and role-specific dashboard templates
```
