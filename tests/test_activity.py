def test_adding_and_completing_task_creates_activity(client):
    client.post("/tasks", data={"title": "Write report", "priority": "High"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/tasks/complete/{task_id}")

    page = client.get("/activity").data.decode()

    assert "Task added: Write report" in page
    assert "Task completed: Write report" in page


def test_deleting_task_is_logged(client):
    client.post("/tasks", data={"title": "Temp", "priority": "Low"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/tasks/delete/{task_id}")

    assert "Task deleted: Temp" in client.get("/activity").data.decode()


def test_activity_page_empty_state(client):
    assert b"No activity yet" in client.get("/activity").data


def test_dashboard_shows_overall_progress(client):
    client.post("/tasks", data={"title": "a", "priority": "Low"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/tasks/complete/{task_id}")

    assert b"100%" in client.get("/").data
