from datetime import date, timedelta

from services.task_service import TaskService


class DeadlineService:
    """Deadline Management module: buckets pending tasks by urgency."""

    WEEK_DAYS = 7

    @staticmethod
    def grouped(db, today=None):
        today = today or date.today()
        week_end = today + timedelta(days=DeadlineService.WEEK_DAYS)

        groups = {
            "overdue": [],
            "today": [],
            "this_week": [],
            "later": [],
            "no_deadline": [],
        }

        for task in TaskService.list_tasks(db, status="pending"):
            if not task["deadline"]:
                groups["no_deadline"].append(task)
                continue

            due = date.fromisoformat(task["deadline"])
            if due < today:
                groups["overdue"].append(task)
            elif due == today:
                groups["today"].append(task)
            elif due <= week_end:
                groups["this_week"].append(task)
            else:
                groups["later"].append(task)

        for key in ("overdue", "today", "this_week", "later"):
            groups[key].sort(key=lambda task: task["deadline"])

        return groups
