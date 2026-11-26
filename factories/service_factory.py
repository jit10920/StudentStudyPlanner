from services.course_service import CourseService
from services.task_service import TaskService


class ServiceFactory:
    @staticmethod
    def get_service(service_type):
        service_type = service_type.lower()

        if service_type == "course":
            return CourseService

        elif service_type == "task":
            return TaskService

        else:
            raise ValueError("Unknown service type")