# Habit Tracker Web App

This is a Flask-based web application that helps users track their daily habits and visualize their progress over time. It is designed to be lightweight, user-friendly, and insightful for anyone looking to improve their routines or build new ones.

## Purpose & Design

**Habit Tracker** is built to help users form and maintain positive daily habits.  
The app allows you to create custom habits, log your progress, and visualize your achievements through interactive charts and annual grid views.  
A key feature is the ability to share your yearly progress grid with friends, supporting motivation and accountability in a private, secure environment.

- **Design:**  
  - Clean, modern interface with responsive design.
  - Secure authentication, CSRF protection, and password reset via email.
  - Data privacy: all user data is private by default and only shared with explicit consent.
  - Visualizations (charts, grids) make progress easy to understand at a glance.
  - Modular codebase for easy maintenance and extension.

## Features

- 📝 Register and log in to your account securely
- ➕ Add and manage custom habits (e.g., sleep, steps, diet)
- 📈 Log daily habit completion with a simple interface
- 📊 Visualize your progress with interactive graphs and annual grid charts
- 🤝 Share your yearly habit grid with other users in-app
- 👀 View shared grids from friends

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-WTF
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (via SQLAlchemy)
- **Interactivity:** AJAX, Fetch API
- **Email Integration:** Gmail API (for password reset)
- **Testing:** unittest, Selenium
- **Version Control:** Git + GitHub

## Getting Started
This section will include how to launch the application.

1. git clone …
2. cd gc_2_app/habit_tracker
3. python -m venv venv && source venv/bin/activate
4. pip install -r requirements.txt
5. export FLASK_APP=app.py          
6. flask db upgrade             
7. (optional) python scripts/seed.py 
8. flask run

> **Note:** This application uses Google Gmail API for sending password reset emails. You'll need two files to make it work:
> - `credentials.json`: Contains your Google API credentials
> - `token.json`: Contains the OAuth2 token for Gmail API access
> 
> These files should be placed in the project root directory. Contact the project maintainer to obtain these files. Do not commit these files to version control as they contain sensitive information.

## Testing (To Be Added)
This section will include how to run unit tests, if applicable.

## Project Structure
```
gc_2_app/                            ← GitHub repository directory
├── habit_tracker/               ← Flask main application folder
│   ├── app/                     ← your main Flask application code
│   │   ├── __init__.py          ← initialization file
│   │   ├── auth/                ← authentication-related routes
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── main/                ← main application routes
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── controller.py    ← business logic
│   │   ├── models.py            ← database models and tables
│   │   ├── forms.py             ← forms for user input
│   │   ├── config.py            ← application configuration
│   │   ├── gmail_api.py         ← Gmail API integration
│   │   ├── templates/           ← HTML templates for rendering pages
│   │   └── static/              ← CSS, images, JavaScript files
│   │       ├── css/             ← CSS files for styling
│   │       ├── js/              ← JavaScript files for interactivity
│   ├── migrations/              ← database migration files
│   ├── scripts/                 ← utility scripts (e.g., seed.py)
│   ├── backups/                 ← database backup files
│   ├── tests/                   ← test files go here
│   ├── requirements.txt         ← list of Python packages
│   └── app.py                   ← main Flask application entry point
├── deliverables/               ← intermediate presentation materials
├── README.md                   ← info about your project
├── venv/                       ← local virtual environment (do not upload to GitHub)
└── .gitignore                  ← ignore development files in venv/ etc.
```

##  Database Management Scripts

To change SQLAlchemy models by updating app/models.py, the following steps needs to be taken
Below is the recommended **"backup → migrate → upgrade → backup → restore"** workflow:

1. Backup (`python scripts/backup_db.py`)
2. Edit your models.py
3. Migrate (`flask db migrate -m "Describe your change here"`)
4. Review & Commit the new script (`git add migrations/versions/<revision_id>_*.py`, `git commit -m "Migration: <brief description>"`)
5. Upgrade (`flask db upgrade`)
6. Backup (`python scripts/backup_db.py`) - This creates a timestamped file in backups/ reflecting your new schema + data. And push your changes to the GitHub.
7. Restore (`python scripts/restore_db.py`) - After they pull your commits (migrations + new backup), they run this to replace their local app/app.db with the freshest backup.

To keep your local SQLite database in sync, backed up, and pre-populated, we provide three helper scripts in the `scripts/` folder:

| Script               | Purpose                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| `backup_db.py`       | Snapshot your current `app/app.db` into a timestamped file under `backups/` |
| `seed.py`            | Create a "seed" user and habit records so a fresh database isn't empty.     |
| `restore_db.py`      | Restore the most recent backup over `app/app.db` for quick rollbacks.       |


### 1. `scripts/backup_db.py`
Creates a copy of your live database at `app/app.db` and writes it to `backups/app_YYYYMMDD_HHMMSS.db`.

```bash
# from the project root (where habit_tracker/ lives)
cd habit_tracker
python scripts/backup_db.py
```
### 2. `scripts/restore_db.py`
This solution for keeping historical data in the system to show proper UI/UX. This script finds latest newest app.db file in backups/
and copy it to app/app.db .

```bash
# from the project root
cd habit_tracker
python scripts/restore_db.py
```

### 3. `scripts/seed.py`
If you need initializes your schema with seed user and starter habits, Run this script by following command from project's root folder.

```bash
# from the project root
cd habit_tracker
python scripts/seed.py
```

## Team Members

| Name                    | UWA ID     | GitHub Username  |
|-------------------------|------------|------------------|
| Siqi Shen               | 24117655   |    saltsoda7     |
| Fiona Wei               | 24610193   |    fifibox       |
| Zaya Batnasan           | 24448191   |  erdenezaya      |
| Divyanshu Brijesh Singh | 24322871   |  Divyanshus123   |

> Note: AI tools (such as ChatGPT) and online resources were used to assist with code, debugging, and documentation in this project.