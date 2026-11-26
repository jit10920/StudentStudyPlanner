
import sqlite3
import pytest
from datetime import date, timedelta
from services.task_service import TaskService


@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    connection.execute(
        "CREATE TABLE courses (id INTEGER PRIMARY KEY, course_name TEXT)"
    )

    connection.execute("""CREATE TABLE tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        course_id INTEGER,
        deadline TEXT,
        priority TEXT,
        status TEXT DEFAULT 'pending'
    )""")

    yield connection

    connection.close()


def test_add_task(db):
    TaskService.add_task(
        db, "Finish lab", "Testing", None, "2030-01-01", "High"
    )

    task = db.execute("SELECT * FROM tasks").fetchone()

    assert task["title"] == "Finish lab"
    assert task["status"] == "pending"


def test_complete_task(db):
    db.execute("INSERT INTO tasks (title) VALUES ('Study')")

    TaskService.complete_task(db, 1)

    assert db.execute(
        "SELECT status FROM tasks WHERE id=1"
    ).fetchone()[0] == "completed"


def test_list_tasks(db):
    TaskService.add_task(db, "Task 1", deadline="2030-01-01")
    TaskService.add_task(db, "Task 2", deadline="2030-01-02")

    tasks = TaskService.list_tasks(db)

    assert len(tasks) == 2


def test_filter_pending_and_completed_tasks(db):
    TaskService.add_task(db, "Pending task")
    TaskService.add_task(db, "Completed task")

    TaskService.complete_task(db, 2)

    pending = TaskService.list_tasks(db, "pending")
    completed = TaskService.list_tasks(db, "completed")

    assert len(pending) == 1
    assert pending[0]["title"] == "Pending task"

    assert len(completed) == 1
    assert completed[0]["title"] == "Completed task"


def test_delete_task(db):
    TaskService.add_task(db, "Delete me")

    TaskService.delete_task(db, 1)

    assert len(TaskService.list_tasks(db)) == 0


def test_task_course_association(db):
    db.execute(
        "INSERT INTO courses (course_name) VALUES ('Software Engineering')"
    )

    TaskService.add_task(db, "Finish project", course_id=1)

    tasks = TaskService.list_tasks(db)

    assert tasks[0]["course_name"] == "Software Engineering"


def test_task_stats(db):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    TaskService.add_task(db, "Overdue task", deadline=yesterday)
    TaskService.add_task(db, "Upcoming task", deadline=tomorrow)
    TaskService.add_task(db, "Completed task", deadline=yesterday)

    TaskService.complete_task(db, 3)

    stats = TaskService.stats(db)

    assert stats["total"] == 3
    assert stats["completed"] == 1
    assert stats["pending"] == 2
    assert stats["overdue"] == 1
