from add_frame_constants import DATABASE

from abc import ABC, abstractmethod
import sqlite3


class AlterDB(ABC):
    """This class defines how classes altering db should look like."""

    prompts = {
        "test_existence": "SElECT class_name FROM classes WHERE class_name = (:class_name);",
        "retrieve_id": "SELECT class_id FROM classes WHERE class_name = (:class_name);",
        "insert_class": "INSERT INTO classes(class_name) VALUES (:class_name);",
        "update_class": "UPDATE classes SET class_name = (:new_class_name) WHERE class_name = (:old_class_name);",
        "insert_student": "INSERT INTO students VALUES (:first_name, :surname, :class_id, :url);"
    }

    # connect to the db
    def __init__(self):
        self.c = sqlite3.connect(DATABASE)
        self.cur = self.c.cursor()

    # functions that are either an intermediate steps or parameters checking
    def fetch_class_id(self, class_name: str) -> int:
        prompt = self.prompts["retrieve_id"]
        self.cur.execute(prompt, {"class_name": class_name})
        class_id = self.cur.fetchone()[0]
        return class_id

    def close_db(self):
        self.c.close()

    def commit(self):
        self.c.commit()

    # function that alters db
    @abstractmethod
    def alter(self) -> None:
        pass
