import pytest

from factories.service_factory import ServiceFactory
from services.course_service import CourseService
from services.task_service import TaskService


def test_get_course_service():
    service = ServiceFactory.get_service("course")
    assert service == CourseService


def test_get_task_service():
    service = ServiceFactory.get_service("task")
    assert service == TaskService


def test_unknown_service():
    with pytest.raises(ValueError):
        ServiceFactory.get_service("unknown")


def test_service_type_case_insensitive():
    service = ServiceFactory.get_service("COURSE")
    assert service == CourseService