
import os
import sqlite3
from pathlib import Path

# STUDY_PLANNER_DB lets a container keep the database on a mounted volume.
DB_PATH = Path(os.environ.get("STUDY_PLANNER_DB", Path(__file__).parent / "study_planner.db"))


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    db = get_db()

    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_code TEXT NOT NULL UNIQUE,
                semester TEXT DEFAULT ''
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                course_id INTEGER,
                deadline TEXT,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'pending',
                FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE SET NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()

    finally:
        db.close()
