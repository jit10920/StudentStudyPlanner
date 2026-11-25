import sqlite3
from services.task_service import TaskService

def make_db():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE courses (id INTEGER PRIMARY KEY, course_name TEXT)")
    db.execute("""CREATE TABLE tasks (
        id INTEGER PRIMARY KEY, title TEXT, description TEXT, course_id INTEGER,
        deadline TEXT, priority TEXT, status TEXT DEFAULT 'pending'
    )""")
    return db

def test_add_task():
    db = make_db()
    TaskService.add_task(db, "Finish lab", "Testing", None, "2030-01-01", "High")
    task = db.execute("SELECT * FROM tasks").fetchone()
    assert task["title"] == "Finish lab"
    assert task["status"] == "pending"

def test_complete_task():
    db = make_db()
    db.execute("INSERT INTO tasks (title) VALUES ('Study')")
    TaskService.complete_task(db, 1)
    assert db.execute("SELECT status FROM tasks WHERE id=1").fetchone()[0] == "completed"
