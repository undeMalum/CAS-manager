from src.database_management import db_manager


def delete_class(class_name: str) -> None:
    # Create the prompt and data
    prompt = """DELETE FROM classes WHERE class_name = (:class_name)"""

    data = {"class_name": class_name}

    # Manage the transaction
    with db_manager.SQLite() as cur:
        cur.execute(prompt, data)


def delete_student(students_id: list[int]) -> None:
    # Create the prompt and data
    prompt = """DELETE FROM students WHERE student_id = (:student_id)"""

    # Manage the transaction
    with db_manager.SQLite() as cur:
        for student_id in students_id:
            data = {"student_id": student_id}
            cur.execute(prompt, data)
