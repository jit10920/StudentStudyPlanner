from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db
from services.course_service import CourseService
from services.task_service import TaskService

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-your-project"

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

    return render_template(
        "courses.html",
        courses=CourseService.list_courses(db)
    )


@app.route("/courses/delete/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    CourseService.delete_course(get_db(), course_id)
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

        flash("Task added successfully.", "success")
        return redirect(url_for("tasks"))

    filter_status = request.args.get("status", "all")

    if filter_status not in ("all", "pending", "completed"):
        filter_status = "all"

    return render_template(
        "tasks.html",
        tasks=TaskService.list_tasks(db, status=filter_status),
        courses=CourseService.list_courses(db),
        filter_status=filter_status
    )


@app.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    db = get_db()

    task = db.execute(
        "SELECT id, status FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        flash("Task not found.", "danger")
    elif task["status"] == "completed":
        flash("Task is already completed.", "info")
    else:
        TaskService.complete_task(db, task_id)
        flash("Task marked as completed.", "success")

    return redirect(url_for("tasks"))


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    db = get_db()

    task = db.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        flash("Task not found.", "danger")
    else:
        TaskService.delete_task(db, task_id)
        flash("Task deleted.", "info")

    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)