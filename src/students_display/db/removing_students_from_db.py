from src.custom_managers import db_manager


def delete_student(student_id: int) -> None:
    # Create the prompt and data
    prompt = """DELETE FROM students WHERE student_id = (:student_id)"""

    data = {"student_id": student_id}

    # Manage the transaction
    with db_manager.SQLite() as cur:
        cur.execute(prompt, data)
