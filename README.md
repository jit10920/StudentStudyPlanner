# Student Study Planner

A simple Flask + SQLite project for the CSE 3206 Software Engineering Sessional reflection assignment.

## Modules
- Course Management
- Task Management
- Deadline Management
- Progress Tracking
- Dashboard

## Setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Tests

```powershell
pytest
pytest --cov=services --cov-report=term-missing
```

This starter is intentionally simple. Extend it for your assignment by adding design patterns, mocks, Selenium, GitHub Actions, report evidence, and your reflection essay.
