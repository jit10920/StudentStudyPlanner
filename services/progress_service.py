class ProgressService:
    """Progress Tracking module: completion statistics per course and overall."""

    @staticmethod
    def by_course(db):
        rows = db.execute(
            """
            SELECT courses.id AS course_id,
                   courses.course_name,
                   courses.course_code,
                   COUNT(tasks.id) AS total,
                   COALESCE(SUM(CASE WHEN tasks.status = 'completed' THEN 1 ELSE 0 END), 0) AS completed
            FROM courses LEFT JOIN tasks ON tasks.course_id = courses.id
            GROUP BY courses.id
            ORDER BY courses.course_name
            """
        ).fetchall()

        return [
            {
                "course_id": row["course_id"],
                "course_name": row["course_name"],
                "course_code": row["course_code"],
                "total": row["total"],
                "completed": row["completed"],
                "percent": ProgressService._percent(row["completed"], row["total"]),
            }
            for row in rows
        ]

    @staticmethod
    def overall_percent(db):
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'completed'"
        ).fetchone()[0]
        return ProgressService._percent(completed, total)

    @staticmethod
    def _percent(completed, total):
        return round(completed * 100 / total) if total else 0
