from datetime import date

class TaskService:
    @staticmethod
    def add_task(db, title, description="", course_id=None, deadline=None, priority="Medium"):
        db.execute(
            """INSERT INTO tasks (title, description, course_id, deadline, priority)
               VALUES (?, ?, ?, ?, ?)""",
            (title, description, course_id, deadline, priority)
        )
        db.commit()

    @staticmethod
    def list_tasks(db, status="all"):
        query = """
            SELECT tasks.*, courses.course_name
            FROM tasks LEFT JOIN courses ON tasks.course_id = courses.id
        """
        if status in ("pending", "completed"):
            query += " WHERE tasks.status = ?"
            return db.execute(query + " ORDER BY deadline", (status,)).fetchall()
        return db.execute(query + " ORDER BY deadline").fetchall()

    @staticmethod
    def complete_task(db, task_id):
        db.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        db.commit()

    @staticmethod
    def delete_task(db, task_id):
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()

    @staticmethod
    def stats(db):
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'").fetchone()[0]
        pending = total - completed
        overdue = db.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND deadline < ?",
            (date.today().isoformat(),)
        ).fetchone()[0]
        return {"total": total, "completed": completed, "pending": pending, "overdue": overdue}
