from unittest.mock import MagicMock, Mock

from events.observers import (
    ActivityLogObserver,
    LogNotifier,
    NotificationObserver,
    TaskEventPublisher,
)


def test_subscribed_observer_receives_event():
    publisher = TaskEventPublisher()
    observer = Mock()
    publisher.subscribe(observer)

    publisher.publish("task_completed", {"title": "Lab report"})

    observer.update.assert_called_once_with("task_completed", {"title": "Lab report"})


def test_unsubscribed_observer_is_not_called():
    publisher = TaskEventPublisher()
    observer = Mock()
    publisher.subscribe(observer)
    publisher.unsubscribe(observer)

    publisher.publish("task_added", {"title": "x"})

    observer.update.assert_not_called()


def test_duplicate_subscription_is_ignored():
    publisher = TaskEventPublisher()
    observer = Mock()
    publisher.subscribe(observer)
    publisher.subscribe(observer)

    publisher.publish("task_added", {"title": "x"})

    assert observer.update.call_count == 1


def test_failing_observer_does_not_block_others():
    publisher = TaskEventPublisher()
    broken = Mock()
    broken.update.side_effect = RuntimeError("boom")
    healthy = Mock()
    publisher.subscribe(broken)
    publisher.subscribe(healthy)

    publisher.publish("task_added", {"title": "x"})

    healthy.update.assert_called_once()


def test_activity_log_observer_writes_with_mocked_db():
    db = MagicMock()
    observer = ActivityLogObserver(lambda: db)

    observer.update("task_completed", {"title": "Quiz prep"})

    sql, params = db.execute.call_args[0]
    assert "INSERT INTO activity_log" in sql
    assert params[0] == "task_completed"
    assert "Quiz prep" in params[1]
    db.commit.assert_called_once()


def test_notification_observer_uses_mocked_notifier():
    notifier = Mock()
    observer = NotificationObserver(notifier)

    observer.update("task_completed", {"title": "Quiz prep"})

    notifier.notify.assert_called_once()
    assert "Quiz prep" in notifier.notify.call_args[0][0]


def test_notification_observer_ignores_non_completion_events():
    notifier = Mock()
    NotificationObserver(notifier).update("task_added", {"title": "x"})

    notifier.notify.assert_not_called()


def test_log_notifier_writes_to_logger(caplog):
    with caplog.at_level("INFO"):
        LogNotifier().notify("hello")

    assert "hello" in caplog.text
