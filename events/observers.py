"""Observer pattern: task events are published, interested parties subscribe."""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

MESSAGES = {
    "task_added": "Task added: {title}",
    "task_completed": "Task completed: {title}",
    "task_deleted": "Task deleted: {title}",
}


class Observer(ABC):
    @abstractmethod
    def update(self, event, data):
        pass


class TaskEventPublisher:
    """Subject. Keeps the task workflow unaware of who reacts to its events."""

    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, event, data):
        for observer in list(self._observers):
            try:
                observer.update(event, data)
            except Exception:  # one bad observer must not break the request
                logger.exception("Observer %r failed on %s", observer, event)


class ActivityLogObserver(Observer):
    """Persists every event into the activity_log table."""

    def __init__(self, db_getter):
        self._db_getter = db_getter

    def update(self, event, data):
        template = MESSAGES.get(event, event)
        message = template.format(title=data.get("title", "(untitled)"))
        db = self._db_getter()
        db.execute(
            "INSERT INTO activity_log (event, message) VALUES (?, ?)",
            (event, message),
        )
        db.commit()


class LogNotifier:
    """Default notifier. A real one (email, push) would be a network dependency."""

    def notify(self, message):
        logger.info(message)


class NotificationObserver(Observer):
    """Sends a notification when a task is completed."""

    def __init__(self, notifier):
        self._notifier = notifier

    def update(self, event, data):
        if event == "task_completed":
            self._notifier.notify(
                MESSAGES["task_completed"].format(title=data.get("title", "(untitled)"))
            )
