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
    return render_template("index.html", stats=stats, tasks=upcoming[:5], courses=courses)


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
    CourseService.delete_course(get_db(), course_id)
    flash("Course deleted.", "info")
    return redirect(url_for("courses"))


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    db = get_db()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        course_id = request.form.get("course_id") or None
        description = request.form.get("description", "").strip()
        deadline = request.form.get("deadline") or None
        priority = request.form.get("priority", "Medium")

        if title:
            TaskService.add_task(db, title, description, course_id, deadline, priority)
            flash("Task added successfully.", "success")
        else:
            flash("Task title is required.", "danger")

        return redirect(url_for("tasks"))

    filter_status = request.args.get("status", "all")

    return render_template(
        "tasks.html",
        tasks=TaskService.list_tasks(db, status=filter_status),
        courses=CourseService.list_courses(db),
        filter_status=filter_status
    )


@app.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    TaskService.complete_task(get_db(), task_id)
    flash("Task marked as completed.", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    TaskService.delete_task(get_db(), task_id)
    flash("Task deleted.", "info")
    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)