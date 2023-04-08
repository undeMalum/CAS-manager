from abc import ABC, abstractmethod

from src.custom_managers import db_manager


class AlterDB(ABC):
    """This class defines how classes altering db should look like."""

    prompts = {
        "test_existence": "SElECT class_name FROM classes WHERE class_name = (:class_name);",
        "retrieve_id": "SELECT class_id FROM classes WHERE class_name = (:class_name);",
        "insert_class": "INSERT INTO classes(class_name) VALUES (:class_name);",
        "update_class": "UPDATE classes SET class_name = (:new_class_name) WHERE class_name = (:old_class_name);",
        "insert_student": """INSERT INTO students(first_name, surname, class_id, url) 
                             VALUES (:first_name, :surname, :class_id, :url);""",
        "update_student": """UPDATE students SET first_name = (:first_name), surname = (:surname),
                             class_id = (:class_id), url = (:url)
                             WHERE student_id = (:student_id)"""
    }

    # connect to the db
    def __init__(self):
        self.connection_with_db = db_manager.SQLite()

    # functions that are either an intermediate steps or parameters checking
    def fetch_class_id(self, class_name: str) -> int:
        # Retrieve query
        prompt = self.prompts["retrieve_id"]

        # Manage connection with the db
        with self.connection_with_db as cur:
            cur.execute(prompt, {"class_name": class_name})
            class_id = cur.fetchone()[0]
            return class_id

    # function that alters db
    @abstractmethod
    def alter(self) -> None:
        pass
