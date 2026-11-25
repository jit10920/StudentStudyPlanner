class CourseService:
    @staticmethod
    def add_course(db, name, code, semester=""):
        db.execute(
            "INSERT INTO courses (course_name, course_code, semester) VALUES (?, ?, ?)",
            (name, code, semester)
        )
        db.commit()

    @staticmethod
    def list_courses(db):
        return db.execute("SELECT * FROM courses ORDER BY course_name").fetchall()

    @staticmethod
    def delete_course(db, course_id):
        db.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        db.commit()
