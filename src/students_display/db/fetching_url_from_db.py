from src.custom_managers import db_manager


def fetch_url(student_id: int) -> str:
    prompt = "SELECT url FROM students WHERE student_id = (:student_id)"
    data = {"student_id": student_id}

    with db_manager.SQLite() as cur:
        cur.execute(prompt, data)

        return cur.fetchone()[0]
