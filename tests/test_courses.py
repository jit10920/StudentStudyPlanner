import sqlite3
from services.course_service import CourseService

def create_db():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY,
            course_name TEXT,
            course_code TEXT,
            semester TEXT
        )
    """)
    return db

def test_add_and_list_course():
    db = create_db()
    CourseService.add_course(db, "Software Engineering", "CSE3206", "3-2")
    courses = CourseService.list_courses(db)

    assert len(courses) == 1
    assert courses[0]["course_code"] == "CSE3206"
    assert courses[0]["course_name"] == "Software Engineering"

def test_list_courses_empty():
    db = create_db()
    courses = CourseService.list_courses(db)

    assert len(courses) == 0

def test_add_multiple_courses():
    db = create_db()
    CourseService.add_course(db, "Software Engineering", "CSE3206", "3-2")
    CourseService.add_course(db, "Artificial Intelligence", "CSE3208", "3-2")

    courses = CourseService.list_courses(db)

    assert len(courses) == 2