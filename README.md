# CircleSync: a Social Life App

A CRUD-based application with two main components:

- **Desktop App**: Built using Python (Tkinter).
- **Web App**: Built using Django, HTML, CSS, and JavaScript.

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Requirements](#requirements)
- [Team Roles](#team-roles)
- [Project Structure](#project-structure)
- [Agile Planning](#agile-planning)

## Overview
This is the final software engineering project following CRUD conventions, featuring:
- A desktop application for managing activities, events, and announcements.
- A web application (in development) to extend functionality online.

## Tech Stack
**Desktop**:
- Python 3.13+
- Tkinter (built-in GUI library)

**Web**:
- Python 3.13+
- Django
- HTML / CSS / JavaScript

## Setup

Follow these steps to get the project running locally.

### 1. Clone the repository

Clone the repo and change into the project directory.

```bash
git clone https://github.com/Dragosharwild/social-life-app.git
cd social-life-app
```

### 2. Create and activate a virtual environment

Create a virtual environment named `venv` and activate it. Use the instructions for your OS and shell.

Windows (PowerShell):

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

Windows (Command Prompt):

```bat
python -m venv venv
venv\Scripts\activate.bat
```

macOS and Linux (bash):

```bash
python3 -m venv venv
source venv/bin/activate
```

Note: If you already use a `.venv` folder, activate that instead (this repo commonly uses `.venv`). On macOS, `python3` is often required instead of `python`.

### 3. Install dependencies

Install the Python packages required by the project.

```bash
pip install -r requirements.txt
```

### 4. Running the applications

Desktop app (GUI):

```bash
python desktop/main.py
```

Expected behavior: Launches the Tkinter UI (CircleSync). You should see the login screen. The app will create/initialize the SQLite database on first run at `desktop/data/circlesync.sqlite`.

Database management tool (CLI):

```bash
python desktop/main.py --cli
```

Expected behavior: Starts an interactive terminal menu to:
- Show DB summary (path, size, tables, row counts)
- View table rows with an optional limit
- Delete the database file (with confirmation)

Web App (Browser):

```bash
python web/manage.py migrate
python web/manage.py runserver
```
Expected behavior: Lauches the web server on http://127.0.0.1:8000/.

## Requirements
### Functional Requirements
- Users can add, edit, delete, and view activities.
- Users can view upcoming events via a calendar.
- Users can post and browse bulletin board announcements.
- Users can access emergency contacts quickly.

### Technical Requirements
- Platform support for Desktop (Tkinter) and Web (Django).
- Modular, well-documented code.
- Version control with GitHub.
- Agile development methodology.

## Team Roles
- Cesar Lozano — Project Manager, Backend Focus
- Efren Carrillo — Sprint Manager, Frontend Focus
- Randy Cantu — Frontend Lead
- Isaac Macias — Backend Lead

## Project Structure
- `desktop/`: Desktop application code (Tkinter).
- `web/`: Web application (Django).
- `shared/`: Code shared between desktop and web.
- `docs/`: Technical documents, UML diagrams, planning, etc.

## Agile Planning
We follow Agile methodology with weekly sprints tracking progress.

### Sprint 1 Goals (Due August 1)
- Set up basic desktop environment with GUI skeleton.
- Upload requirements and planning docs.
- Establish roles and repository structure.

### Sprint 2 Goals (Due August 8)
- Implement sign-up & login pages with data storage.
- Add functionality to create and join inner circles.
- Track number of members per circle and identify circle creator.

### Sprint 3 Goals (Due August 15)
- Refactor code into a layered architecture focused on modularity.
- Have UI actually display DB data instead of mock data.
- Set up the web environment with Django bootstrap.

### Sprint 4 Goals (Due August 22)
- 