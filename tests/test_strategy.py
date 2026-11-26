from strategies.deadline_strategy import DeadlineStrategy
from strategies.priority_strategy import PriorityStrategy
from strategies.default_strategy import DefaultStrategy


def test_deadline_strategy():
    tasks = [
        {"title": "Task A", "deadline": "2026-12-10", "priority": "Low"},
        {"title": "Task B", "deadline": "2026-12-01", "priority": "High"},
        {"title": "Task C", "deadline": None, "priority": "Medium"},
        {"title": "Task D", "deadline": "2026-12-05", "priority": "Medium"}
    ]

    result = DeadlineStrategy().sort(tasks)

    assert [task["title"] for task in result] == [
        "Task B", "Task D", "Task A", "Task C"
    ]


def test_priority_strategy():
    tasks = [
        {"title": "Task A", "deadline": "2026-12-01", "priority": "Low"},
        {"title": "Task B", "deadline": "2026-12-02", "priority": "High"},
        {"title": "Task C", "deadline": "2026-12-03", "priority": "Medium"}
    ]

    result = PriorityStrategy().sort(tasks)

    assert [task["title"] for task in result] == [
        "Task B", "Task C", "Task A"
    ]


def test_default_strategy():
    tasks = [
        {"title": "Task A", "deadline": "2026-12-10", "priority": "Low"},
        {"title": "Task B", "deadline": "2026-12-01", "priority": "High"},
        {"title": "Task C", "deadline": None, "priority": "Medium"}
    ]

    result = DefaultStrategy().sort(tasks)

    assert [task["title"] for task in result] == [
        "Task A", "Task B", "Task C"
    ]

    assert result == tasks
