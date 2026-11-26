import importlib
import pytest
import database


@pytest.fixture
def app_module(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")

    module = importlib.import_module("app")
    module = importlib.reload(module)

    yield module


@pytest.fixture
def client(app_module):
    return app_module.app.test_client()


@pytest.fixture
def seed_tasks(app_module):
    db = app_module.get_db()

    db.execute(
        "INSERT INTO tasks (title, deadline, priority, status) VALUES (?, ?, ?, ?)",
        ("Task A", "2026-12-10", "Low", "pending")
    )

    db.execute(
        "INSERT INTO tasks (title, deadline, priority, status) VALUES (?, ?, ?, ?)",
        ("Task B", "2026-12-01", "High", "pending")
    )

    db.execute(
        "INSERT INTO tasks (title, deadline, priority, status) VALUES (?, ?, ?, ?)",
        ("Task C", None, "Medium", "pending")
    )

    db.execute(
        "INSERT INTO tasks (title, deadline, priority, status) VALUES (?, ?, ?, ?)",
        ("Task D", "2026-12-05", "Medium", "completed")
    )

    db.commit()
    db.close()


def get_task_positions(response, titles):
    html = response.data.decode("utf-8")
    return [html.index(title) for title in titles]


def test_tasks_page_loads(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert b"Task Management" in response.data


def test_deadline_sorting(client, seed_tasks):
    response = client.get("/tasks?sort=deadline")

    assert response.status_code == 200

    positions = get_task_positions(
        response,
        ["Task B", "Task D", "Task A", "Task C"]
    )

    assert positions == sorted(positions)


def test_priority_sorting(client, seed_tasks):
    response = client.get("/tasks?sort=priority")

    assert response.status_code == 200

    positions = get_task_positions(
        response,
        ["Task B", "Task C", "Task A"]
    )

    assert positions == sorted(positions)


def test_default_sorting(client, seed_tasks):
    response = client.get("/tasks?sort=default")

    assert response.status_code == 200

    positions = get_task_positions(
        response,
        ["Task A", "Task B", "Task C", "Task D"]
    )

    assert positions == sorted(positions)


def test_invalid_sort_uses_default(client, seed_tasks):
    response = client.get("/tasks?sort=invalid")

    assert response.status_code == 200

    positions = get_task_positions(
        response,
        ["Task A", "Task B", "Task C", "Task D"]
    )

    assert positions == sorted(positions)


def test_completed_filter_with_deadline_sort(client, seed_tasks):
    response = client.get("/tasks?status=completed&sort=deadline")

    assert response.status_code == 200
    assert b"Task D" in response.data

    assert b"Task A" not in response.data
    assert b"Task B" not in response.data
    assert b"Task C" not in response.data
    
def test_dashboard_loads(client):
    response = client.get("/")

    assert response.status_code == 200


def test_courses_page_loads(client):
    response = client.get("/courses")

    assert response.status_code == 200


def test_add_course_success(client):
    response = client.post("/courses", data={
        "course_name": "Software Engineering",
        "course_code": "CSE3206",
        "semester": "3-2"
    })

    assert response.status_code == 302

    response = client.get("/courses")

    assert b"Software Engineering" in response.data


def test_add_course_without_required_fields(client):
    response = client.post("/courses", data={
        "course_name": "",
        "course_code": ""
    })

    assert response.status_code == 302


def test_delete_course(client):
    client.post("/courses", data={
        "course_name": "Software Engineering",
        "course_code": "CSE3206",
        "semester": "3-2"
    })

    response = client.post("/courses/delete/1")

    assert response.status_code == 302
