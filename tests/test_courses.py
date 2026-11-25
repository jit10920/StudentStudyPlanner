import sqlite3
from services.course_service import CourseService

def test_add_and_list_course():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE courses (id INTEGER PRIMARY KEY, course_name TEXT, course_code TEXT, semester TEXT)")
    CourseService.add_course(db, "Software Engineering", "CSE3206", "3-2")
    courses = CourseService.list_courses(db)
    assert len(courses) == 1
    assert courses[0]["course_code"] == "CSE3206"
