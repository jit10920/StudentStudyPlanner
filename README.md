# Student Study Planner

A simple Flask + SQLite project for the CSE 3206 Software Engineering Sessional reflection assignment.

## Modules
- Course Management
- Task Management
- Deadline Management (`/deadlines`)
- Progress Tracking (`/progress`)
- Activity Log (`/activity`, filled by the Observer pattern)
- Dashboard
- JSON API with Swagger docs (`/api/docs`)

## Design patterns
Factory (`factories/`), Strategy (`strategies/`), Observer (`events/`). See `docs/REPORT.md` for the UML diagram and rejected alternatives.

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
pytest --ignore=tests/e2e --cov        # unit tests + coverage
pytest tests/e2e                        # Selenium tests (needs Chrome)
```

CI (GitHub Actions) runs both on every push and pull request.

## Documentation
- `docs/REPORT.md` – requirements, process model, patterns, UML, tests, new tool
- `docs/REFLECTION.md` – learning log and reflection essay


## Git workflow for the final increment
Branch names: `feature/deadline-progress`, `feature/observer-activity-log`, `feature/openapi-docs`, `feature/selenium-ci`. Each is merged into `main` by a pull request. One pull request should be reviewed with requested changes (revised before merge) to show the review process.

## Running the tests
Run the unit tests with coverage: `pytest --ignore=tests/e2e --cov`
