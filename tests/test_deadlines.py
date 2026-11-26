from datetime import date

from services.deadline_service import DeadlineService
from services.task_service import TaskService

TODAY = date(2026, 11, 26)  # Thursday


def _add(db, title, deadline, status="pending"):
    TaskService.add_task(db, title, deadline=deadline)
    task = [t for t in TaskService.list_tasks(db) if t["title"] == title][0]
    if status == "completed":
        TaskService.complete_task(db, task["id"])


def _titles(rows):
    return [row["title"] for row in rows]


def test_groups_pending_tasks_by_urgency(app_module):
    db = app_module.get_db()
    _add(db, "late", "2026-11-20")
    _add(db, "today", "2026-11-26")
    _add(db, "soon", "2026-11-30")
    _add(db, "far", "2026-12-25")
    _add(db, "whenever", None)

    groups = DeadlineService.grouped(db, today=TODAY)

    assert _titles(groups["overdue"]) == ["late"]
    assert _titles(groups["today"]) == ["today"]
    assert _titles(groups["this_week"]) == ["soon"]
    assert _titles(groups["later"]) == ["far"]
    assert _titles(groups["no_deadline"]) == ["whenever"]


def test_completed_tasks_are_excluded(app_module):
    db = app_module.get_db()
    _add(db, "done", "2026-11-01", status="completed")

    groups = DeadlineService.grouped(db, today=TODAY)

    assert all(rows == [] for rows in groups.values())


def test_week_boundary_is_seven_days_inclusive(app_module):
    db = app_module.get_db()
    _add(db, "day7", "2026-12-03")
    _add(db, "day8", "2026-12-04")

    groups = DeadlineService.grouped(db, today=TODAY)

    assert _titles(groups["this_week"]) == ["day7"]
    assert _titles(groups["later"]) == ["day8"]


def test_each_group_sorted_by_deadline(app_module):
    db = app_module.get_db()
    _add(db, "b", "2026-12-02")
    _add(db, "a", "2026-11-28")

    groups = DeadlineService.grouped(db, today=TODAY)

    assert _titles(groups["this_week"]) == ["a", "b"]


def test_deadlines_page_renders(client):
    response = client.get("/deadlines")

    assert response.status_code == 200
    assert b"Deadline Management" in response.data
