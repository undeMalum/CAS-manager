from src.custom_managers import db_manager


def delete_student(class_name: int) -> None:
    # Create the prompt and data
    prompt = """DELETE FROM classes WHERE class_name = (:class_name)"""

    data = {"class_name": class_name}

    # Manage the transaction
    with db_manager.SQLite() as cur:
        cur.execute(prompt, data)
