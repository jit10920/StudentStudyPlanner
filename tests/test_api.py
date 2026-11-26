import re

from openapi_spec_validator import validate


def test_openapi_spec_is_valid(client):
    spec = client.get("/api/openapi.json").get_json()

    validate(spec)  # raises if the document breaks the OpenAPI 3 schema


def test_every_documented_operation_has_a_route(client, app_module):
    spec = client.get("/api/openapi.json").get_json()
    rules = {}
    for rule in app_module.app.url_map.iter_rules():
        path = re.sub(r"<(?:int:)?(\w+)>", r"{\1}", rule.rule)
        rules.setdefault(path, set()).update(rule.methods)

    for path, operations in spec["paths"].items():
        assert path in rules, f"{path} is documented but not implemented"
        for method in operations:
            assert method.upper() in rules[path], f"{method} {path} not implemented"


def test_swagger_ui_page_loads(client):
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert b"swagger-ui" in response.data


def test_create_and_list_task(client):
    created = client.post("/api/tasks", json={"title": "Read chapter 4", "priority": "High"})

    assert created.status_code == 201
    assert created.get_json()["title"] == "Read chapter 4"

    listed = client.get("/api/tasks").get_json()
    assert [t["title"] for t in listed] == ["Read chapter 4"]


def test_create_task_requires_title(client):
    response = client.post("/api/tasks", json={"priority": "High"})

    assert response.status_code == 400
    assert "title" in response.get_json()["error"]


def test_create_task_rejects_bad_priority(client):
    response = client.post("/api/tasks", json={"title": "x", "priority": "Urgent"})

    assert response.status_code == 400


def test_create_task_rejects_unknown_course(client):
    response = client.post("/api/tasks", json={"title": "x", "course_id": 999})

    assert response.status_code == 400


def test_filter_tasks_by_status(client):
    client.post("/api/tasks", json={"title": "one"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/api/tasks/{task_id}/complete")

    assert client.get("/api/tasks?status=pending").get_json() == []
    assert len(client.get("/api/tasks?status=completed").get_json()) == 1


def test_complete_task_publishes_event(client, app_module, monkeypatch):
    from unittest.mock import Mock

    publisher = Mock()
    monkeypatch.setattr(app_module, "event_publisher", publisher)
    client.post("/api/tasks", json={"title": "mocked"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]

    response = client.post(f"/api/tasks/{task_id}/complete")

    assert response.status_code == 200
    events = [call.args[0] for call in publisher.publish.call_args_list]
    assert events == ["task_added", "task_completed"]


def test_complete_missing_task_is_404(client):
    assert client.post("/api/tasks/999/complete").status_code == 404


def test_courses_and_progress_endpoints(client, app_module):
    app_module.CourseService.add_course(app_module.get_db(), "Networks", "CSE3203")
    course = client.get("/api/courses").get_json()[0]
    client.post("/api/tasks", json={"title": "t", "course_id": course["id"]})

    progress = client.get("/api/progress").get_json()

    assert progress["overall_percent"] == 0
    assert progress["courses"][0]["total"] == 1
