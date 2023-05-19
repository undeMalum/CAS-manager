from src.database_management import db_manager


def fetch_url(students_id: list[int]) -> list[str]:
    prompt = "SELECT url FROM students WHERE student_id = (:student_id)"

    with db_manager.SQLite() as cur:
        ids = []
        for student_id in students_id:
            data = {"student_id": student_id}
            cur.execute(prompt, data)
            ids.append(cur.fetchone()[0])

        return ids
