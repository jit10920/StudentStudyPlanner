from services.course_service import CourseService
from services.progress_service import ProgressService
from services.task_service import TaskService


def _db(app_module):
    return app_module.get_db()


def test_progress_empty_when_no_courses(app_module):
    db = _db(app_module)
    assert ProgressService.by_course(db) == []
    assert ProgressService.overall_percent(db) == 0


def test_course_with_no_tasks_is_zero_percent(app_module):
    db = _db(app_module)
    CourseService.add_course(db, "Networks", "CSE3203", "3-2")

    result = ProgressService.by_course(db)

    assert len(result) == 1
    assert result[0]["total"] == 0
    assert result[0]["percent"] == 0


def test_progress_percent_per_course(app_module):
    db = _db(app_module)
    CourseService.add_course(db, "Networks", "CSE3203")
    course_id = CourseService.list_courses(db)[0]["id"]

    for title in ("a", "b", "c", "d"):
        TaskService.add_task(db, title, course_id=course_id)
    tasks = TaskService.list_tasks(db)
    TaskService.complete_task(db, tasks[0]["id"])

    result = ProgressService.by_course(db)[0]

    assert result["total"] == 4
    assert result["completed"] == 1
    assert result["percent"] == 25


def test_overall_percent_counts_tasks_without_course(app_module):
    db = _db(app_module)
    TaskService.add_task(db, "loose 1")
    TaskService.add_task(db, "loose 2")
    TaskService.complete_task(db, TaskService.list_tasks(db)[0]["id"])

    assert ProgressService.overall_percent(db) == 50


def test_progress_page_renders(client):
    response = client.get("/progress")

    assert response.status_code == 200
    assert b"Progress Tracking" in response.data
