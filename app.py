
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, g, has_app_context
)

from database import init_db, get_db as create_db
from factories.service_factory import ServiceFactory

from strategies.deadline_strategy import DeadlineStrategy
from strategies.priority_strategy import PriorityStrategy
from strategies.default_strategy import DefaultStrategy

from events.observers import (
    TaskEventPublisher, ActivityLogObserver,
    NotificationObserver, LogNotifier
)


CourseService = ServiceFactory.get_service("course")
TaskService = ServiceFactory.get_service("task")
ProgressService = ServiceFactory.get_service("progress")
DeadlineService = ServiceFactory.get_service("deadline")

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-your-project"


def get_db():
    if not has_app_context():
        return create_db()

    if "db" not in g:
        g.db = create_db()

    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


event_publisher = TaskEventPublisher()
event_publisher.subscribe(ActivityLogObserver(get_db))
event_publisher.subscribe(NotificationObserver(LogNotifier()))

init_db()


@app.route("/")
def dashboard():
    db = get_db()

    stats = TaskService.stats(db)
    upcoming = TaskService.list_tasks(db, status="pending")
    courses = CourseService.list_courses(db)

    return render_template(
        "index.html",
        stats=stats,
        overall_percent=ProgressService.overall_percent(db),
        tasks=upcoming[:5],
        courses=courses
    )


@app.route("/courses", methods=["GET", "POST"])
def courses():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("course_name", "").strip()
        code = request.form.get("course_code", "").strip()
        semester = request.form.get("semester", "").strip()

        if name and code:
            CourseService.add_course(db, name, code, semester)
            flash("Course added successfully.", "success")
        else:
            flash("Course name and code are required.", "danger")

        return redirect(url_for("courses"))

    search_query = request.args.get("q", "").strip()

    course_list = (
        CourseService.search_courses(db, search_query)
        if search_query
        else CourseService.list_courses(db)
    )

    return render_template(
        "courses.html",
        courses=course_list,
        search_query=search_query
    )


@app.route("/courses/delete/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    db = get_db()

    CourseService.delete_course(db, course_id)

    flash("Course deleted.", "info")

    return redirect(url_for("courses"))


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    db = get_db()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        deadline = request.form.get("deadline") or None
        priority = request.form.get("priority", "Medium")
        course_id = request.form.get("course_id") or None

        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for("tasks"))

        if priority not in ("Low", "Medium", "High"):
            flash("Invalid priority selected.", "danger")
            return redirect(url_for("tasks"))

        if course_id:
            try:
                course_id = int(course_id)
            except ValueError:
                flash("Invalid course selected.", "danger")
                return redirect(url_for("tasks"))

            courses_list = CourseService.list_courses(db)
            valid_course_ids = [course["id"] for course in courses_list]

            if course_id not in valid_course_ids:
                flash("Selected course does not exist.", "danger")
                return redirect(url_for("tasks"))

        TaskService.add_task(
            db, title, description, course_id, deadline, priority
        )
        event_publisher.publish("task_added", {"title": title})

        flash("Task added successfully.", "success")

        return redirect(url_for("tasks"))

    filter_status = request.args.get("status", "all")

    if filter_status not in ("all", "pending", "completed"):
        filter_status = "all"

    sort_by = request.args.get("sort", "default")

    strategies = {
        "deadline": DeadlineStrategy(),
        "priority": PriorityStrategy(),
        "default": DefaultStrategy()
    }

    if sort_by not in strategies:
        sort_by = "default"

    task_list = TaskService.list_tasks(db, status=filter_status)
    task_list = strategies[sort_by].sort(task_list)

    return render_template(
        "tasks.html",
        tasks=task_list,
        courses=CourseService.list_courses(db),
        filter_status=filter_status,
        sort_by=sort_by
    )


@app.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    db = get_db()

    task = db.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        flash("Task not found.", "danger")

    elif task["status"] == "completed":
        flash("Task is already completed.", "info")

    else:
        TaskService.complete_task(db, task_id)
        event_publisher.publish("task_completed", {"id": task_id, "title": task["title"]})
        flash("Task marked as completed.", "success")

    return redirect(url_for("tasks"))


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    db = get_db()

    task = db.execute(
        "SELECT id, title FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        flash("Task not found.", "danger")

    else:
        TaskService.delete_task(db, task_id)
        event_publisher.publish("task_deleted", {"id": task_id, "title": task["title"]})
        flash("Task deleted.", "info")

    return redirect(url_for("tasks"))


@app.route("/progress")
def progress():
    db = get_db()

    return render_template(
        "progress.html",
        courses=ProgressService.by_course(db),
        overall_percent=ProgressService.overall_percent(db)
    )


@app.route("/deadlines")
def deadlines():
    db = get_db()

    return render_template(
        "deadlines.html",
        groups=DeadlineService.grouped(db)
    )


@app.route("/activity")
def activity():
    db = get_db()

    entries = db.execute(
        "SELECT event, message, created_at FROM activity_log ORDER BY id DESC LIMIT 50"
    ).fetchall()

    return render_template("activity.html", entries=entries)


if __name__ == "__main__":
    app.run(debug=True)
