"""Hand-written OpenAPI 3 description of the JSON API, served at /api/openapi.json."""

_task = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "course_id": {"type": "integer", "nullable": True},
        "course_name": {"type": "string", "nullable": True},
        "deadline": {"type": "string", "format": "date", "nullable": True},
        "priority": {"type": "string", "enum": ["Low", "Medium", "High"]},
        "status": {"type": "string", "enum": ["pending", "completed"]},
    },
}

_error = {
    "type": "object",
    "properties": {"error": {"type": "string"}},
    "required": ["error"],
}


def _json(schema_ref):
    return {"application/json": {"schema": schema_ref}}


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Student Study Planner API",
        "version": "1.0.0",
        "description": "JSON API for courses, tasks and progress.",
    },
    "paths": {
        "/api/courses": {
            "get": {
                "summary": "List courses",
                "responses": {
                    "200": {
                        "description": "All courses",
                        "content": _json({"type": "array", "items": {"$ref": "#/components/schemas/Course"}}),
                    }
                },
            }
        },
        "/api/tasks": {
            "get": {
                "summary": "List tasks",
                "parameters": [
                    {
                        "name": "status",
                        "in": "query",
                        "schema": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Matching tasks",
                        "content": _json({"type": "array", "items": {"$ref": "#/components/schemas/Task"}}),
                    },
                    "400": {"description": "Invalid status", "content": _json({"$ref": "#/components/schemas/Error"})},
                },
            },
            "post": {
                "summary": "Create a task",
                "requestBody": {
                    "required": True,
                    "content": _json({"$ref": "#/components/schemas/NewTask"}),
                },
                "responses": {
                    "201": {"description": "Created task", "content": _json({"$ref": "#/components/schemas/Task"})},
                    "400": {"description": "Validation error", "content": _json({"$ref": "#/components/schemas/Error"})},
                },
            },
        },
        "/api/tasks/{task_id}/complete": {
            "post": {
                "summary": "Mark a task completed",
                "parameters": [
                    {"name": "task_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {"description": "Task completed"},
                    "404": {"description": "Task not found", "content": _json({"$ref": "#/components/schemas/Error"})},
                },
            }
        },
        "/api/progress": {
            "get": {
                "summary": "Progress overall and per course",
                "responses": {
                    "200": {
                        "description": "Progress summary",
                        "content": _json({"$ref": "#/components/schemas/Progress"}),
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Error": _error,
            "Task": _task,
            "Course": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "course_name": {"type": "string"},
                    "course_code": {"type": "string"},
                    "semester": {"type": "string"},
                },
            },
            "NewTask": {
                "type": "object",
                "required": ["title"],
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "course_id": {"type": "integer"},
                    "deadline": {"type": "string", "format": "date"},
                    "priority": {"type": "string", "enum": ["Low", "Medium", "High"], "default": "Medium"},
                },
            },
            "Progress": {
                "type": "object",
                "properties": {
                    "overall_percent": {"type": "integer"},
                    "courses": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "course_id": {"type": "integer"},
                                "course_name": {"type": "string"},
                                "course_code": {"type": "string"},
                                "total": {"type": "integer"},
                                "completed": {"type": "integer"},
                                "percent": {"type": "integer"},
                            },
                        },
                    },
                },
            },
        }
    },
}

SWAGGER_UI_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Study Planner API docs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>SwaggerUIBundle({url: "/api/openapi.json", dom_id: "#swagger-ui"});</script>
</body>
</html>
"""
