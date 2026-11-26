
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "study_planner.db"


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

        db.commit()

    finally:
        db.close()
