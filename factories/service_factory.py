from services.course_service import CourseService
from services.task_service import TaskService
from services.progress_service import ProgressService
from services.deadline_service import DeadlineService


class ServiceFactory:
    @staticmethod
    def get_service(service_type):
        service_type = service_type.lower()

        if service_type == "course":
            return CourseService

        elif service_type == "task":
            return TaskService

        elif service_type == "progress":
            return ProgressService

        elif service_type == "deadline":
            return DeadlineService

        else:
            raise ValueError("Unknown service type")