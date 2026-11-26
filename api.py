"""JSON REST API plus its OpenAPI (Swagger) documentation."""
from flask import Blueprint, jsonify, request

from openapi import OPENAPI_SPEC, SWAGGER_UI_HTML

PRIORITIES = ("Low", "Medium", "High")


def _row(row):
    return {key: row[key] for key in row.keys()}


def create_api_blueprint(get_db, course_service, task_service, progress_service, publish):
    api = Blueprint("api", __name__, url_prefix="/api")

    @api.get("/openapi.json")
    def openapi_spec():
        return jsonify(OPENAPI_SPEC)

    @api.get("/docs")
    def docs():
        return SWAGGER_UI_HTML

    @api.get("/courses")
    def list_courses():
        return jsonify([_row(c) for c in course_service.list_courses(get_db())])

    @api.get("/tasks")
    def list_tasks():
        status = request.args.get("status", "all")
        if status not in ("all", "pending", "completed"):
            return jsonify({"error": "status must be all, pending or completed"}), 400
        return jsonify([_row(t) for t in task_service.list_tasks(get_db(), status=status)])

    @api.post("/tasks")
    def create_task():
        db = get_db()
        body = request.get_json(silent=True) or {}

        title = str(body.get("title", "")).strip()
        if not title:
            return jsonify({"error": "title is required"}), 400

        priority = body.get("priority", "Medium")
        if priority not in PRIORITIES:
            return jsonify({"error": "priority must be Low, Medium or High"}), 400

        course_id = body.get("course_id")
        if course_id is not None:
            valid_ids = [c["id"] for c in course_service.list_courses(db)]
            if course_id not in valid_ids:
                return jsonify({"error": "course_id does not exist"}), 400

        task_service.add_task(
            db, title, body.get("description", ""), course_id,
            body.get("deadline"), priority
        )
        publish("task_added", {"title": title})

        created = task_service.list_tasks(db)[-1]
        return jsonify(_row(created)), 201

    @api.post("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        db = get_db()
        task = db.execute(
            "SELECT id, title FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            return jsonify({"error": "task not found"}), 404

        task_service.complete_task(db, task_id)
        publish("task_completed", {"id": task_id, "title": task["title"]})
        return jsonify({"id": task_id, "status": "completed"})

    @api.get("/progress")
    def progress():
        db = get_db()
        return jsonify({
            "overall_percent": progress_service.overall_percent(db),
            "courses": progress_service.by_course(db),
        })

    return api
